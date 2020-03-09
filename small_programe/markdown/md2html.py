"""
https://www.shiyanlou.com/courses/708
一个简单的markdown解析器
"""
import os
import re
import sys
from enum import Enum
from functools import reduce


def main():
    run("doc_template.md", "translation_result.html")


def run(source_name, dest_name):
    _, suffix = os.path.splitext(source_name)
    if suffix not in [".md", ".markdown", ".mdown", "mkd"]:
        print("Error: the file should be in markdown format")
        sys.exit(1)

    parser = MDParser(source_name, dest_name)
    parser.run()


HEAD_PART = """
<style type="text/css">
    div {
        display: block;
        font-family: "Times New Roman", Georgia, Serif;
    }
    
    table, tr, td{
        border:1px solid #ccc;
    }

    blockquote, code{
        background:#ccc;
    }

    #wrapper {
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
    }

    #left {
        float: left;
        width: 10%;
        height: 100%;
    }

    #second {
        float: left;
        width: 80%;
        height: 100%;
    }

    #right {
        float: left;
        width: 10%;
        height: 100%;
    }
</style>
<div id="wrapper">
    <div id="left"></div>
    <div id="second">
"""
END_PART = '</br></br></div><div id="right"></div></div>'

# 表状态
class TABLE(Enum):
    Init = 1
    Format = 2
    Table = 3


# 有序序列状态
class ORDERLIST(Enum):
    Init = 1
    List = 2


# 块状态
class BLOCK(Enum):
    Init = 1
    Block = 2
    CodeBlock = 3


class MDParser:
    is_normal = True
    is_code = False
    table_state = TABLE.Init
    block_state = BLOCK.Init
    orderList_state = ORDERLIST.Init
    temp_table_first_line = []
    temp_table_first_line_str = ""

    def __init__(self, source_file, dest_file):
        self.source_file = source_file
        self.dest_file = dest_file

    def run(self):
        self.source = open(self.source_file, "r")
        self.dest = open(self.dest_file, "w")
        self.dest.write(HEAD_PART)

        for line in self.source:
            result = self.parse(line)
            if result:
                self.dest.write(result)

        self.dest.write(END_PART)
        self.dest.close()
        self.source.close()

    def parse(self, line):
        self.is_normal = True
        result = line

        #  解析当前line状态
        result = self.get_state(line)

        if self.block_state == BLOCK.Block:
            return result

        # 处理标题 ###
        title_rank = 0
        for i in range(6, 0, -1):
            if line[:i] == "#" * i:
                title_rank = i
                break
        if title_rank != 0:
            result = self.handle_title(line, title_rank)
            return result

        # 处理分割线标记 --
        if len(line) > 2 and self.all_same(line[:-1], "-") and line[-1] == "\n":
            result = "<hr>"
            return result

        # 处理无序列表
        unorderd = ["+", "-", "*"]
        if result != "" and result[0] in unorderd:
            result = self.handle_unorderd(result)
            self.is_normal = False

        f = line[0]
        count = 0
        sys_q = False
        while f == ">":
            count += 1
            f = line[count]
            sys_q = True
        if sys_q:
            result = (
                '<blockquote style="color:#8fbc8f"> ' * count
                + "<b>"
                + line[count:]
                + "</b>"
                + "</blockquote>" * count
            )
            self.is_normal = False

        # 处理特殊标记，比如 ***, ~~~
        result = self.handle_token(result)

        # 解析图像链接
        result = self.handle_img_link(result)
        pa = re.compile(r"^(\s)*$")
        a = pa.match(line)
        if line[-1] == "\n" and self.is_normal == True and not a:
            result += "</br>"

        return result

    def get_state(self, line):
        """判断当前读取的这一行，是否在一个代码块、序列或者表格中"""
        result = line
        # 匹配块标识
        pattern = re.compile(r"```(\s)*\n")
        a = pattern.match(line)

        # 普通块
        if a and self.block_state == BLOCK.Init:
            result = "<blockquote>"
            self.block_state = BLOCK.Block
            self.is_normal = False
        # 特殊代码块
        elif (
            len(line) > 4
            and line[0:3] == "```"
            and (line[3:9] == "python" or line[3:6] == "c++" or line[3:4] == "c")
            and self.block_state == BLOCK.Init
        ):
            self.block_state = BLOCK.Block
            result = "<code></br>"
            self.is_code = True
            self.is_normal = False
        # 块结束
        elif self.block_state == BLOCK.Block and line == "```\n":
            if self.is_code:
                result = "</code>"
            else:
                result = "</blockquote>"
            self.block_state = BLOCK.Init
            self.is_code = False
            self.is_normal = False
        elif self.block_state == BLOCK.Block:
            pattern = re.compile(r"[\n\r\v\f\ ]")
            result = pattern.sub("&nbsp", result)
            pattern = re.compile(r"\t")
            result = pattern.sub("&nbsp" * 4, result)
            result = "<span>" + result + "</span></br>"
            self.is_normal = False

        # 解析有序序列
        if (
            len(line) > 2
            and line[0].isdigit()
            and line[1] == "."
            and self.orderList_state == ORDERLIST.Init
        ):
            self.orderList_state = ORDERLIST.List
            result = "<ol><li>" + line[2:] + "</li>"
            self.is_normal = False
        elif (
            len(line) > 2
            and line[0].isdigit()
            and line[1] == "."
            and self.orderList_state == ORDERLIST.List
        ):
            result = "<li>" + line[2:] + "</li>"
            self.is_normal = False
        elif self.orderList_state == ORDERLIST.List and (
            len(line) <= 2 or line[0].isdigit() == False or line[1] != "."
        ):
            result = "</ol>" + line
            self.orderList_state = ORDERLIST.Init

        # 解析表格
        pattern = re.compile(r"^((.+)\|)+((.+))$")
        match = pattern.match(line)
        if match:
            l = line.split("|")
            l[-1] = l[-1][:-1]
            # 将空字符弹出列表
            if l[0] == "":
                l.pop(0)
            if l[-1] == "":
                l.pop(-1)
            if self.table_state == TABLE.Init:
                self.table_state = TABLE.Format
                self.temp_table_first_line = l
                self.temp_table_first_line_str = line
                result = ""
            elif self.table_state == TABLE.Format:
                # 如果是表头与表格主题的分割线
                if reduce(
                    lambda a, b: a and b, [self.all_same(i, "-") for i in l], True
                ):
                    self.table_state = TABLE.Table
                    result = "<table><thread><tr>"
                    self.is_normal = False

                    # 添加表头
                    for i in self.temp_table_first_line:
                        result += "<th>" + i + "</th>"
                    result += "</tr>"
                    result += "</thread><tbody>"
                    self.is_normal = False
                else:
                    result = temp_table_first_line_str + "</br>" + line
                    self.table_state = TABLE.Init

            elif self.table_state == TABLE.Table:
                result = "<tr>"
                for i in l:
                    result += "<td>" + i + "</td>"
                result += "</tr>"

        elif self.table_state == TABLE.Table:
            self.table_state = TABLE.Init
            result = "</tbody></table>" + result
        elif self.table_state == TABLE.Format:
            pass

        return result

    # 　判断 lst 是否全由字符 sym 构成
    @staticmethod
    def all_same(lst, sym):
        return not lst or sym * len(lst) == lst

    # 处理标题
    @staticmethod
    def handle_title(s, n):
        temp = "<h" + repr(n) + ">" + s[n:] + "</h" + repr(n) + ">"
        return temp

    # 处理无序列表
    @staticmethod
    def handle_unorderd(s):
        s = "<ul><li>" + s[1:]
        s += "</li></ul>"
        return s

    # 处理特殊标识，比如 **, *, ~~
    def handle_token(self, s):
        l = ["b", "i", "S"]
        j = 0
        pt = {
            "*": "\*([^\*]*)\*",
            "~~": "\~\~([^\~\~]*)\~\~",
            "**": "\*\*([^\*\*]*)\*\*",
        }
        for key, value in pt.items():
            pattern = re.compile(value)
            match = pattern.finditer(s)
            k = 0
            for a in match:
                if a:
                    content = a.group(1)
                    x, y = a.span()
                    c = 5 if key == "*" else 3
                    s = (
                        s[: x + c * k]
                        + "<"
                        + l[j]
                        + ">"
                        + content
                        + "</"
                        + l[j]
                        + ">"
                        + s[y + c * k :]
                    )
                    k += 1
            j += 1
        return s

    
    # 处理链接
    @staticmethod
    def handle_img_link(s):
        # 超链接
        pattern = re.compile(r"\\\[(.*)\]\((.*)\)")
        match = pattern.finditer(s)
        for a in match:
            if a:
                text, url = a.group(1, 2)
                x, y = a.span()
                s = (
                    s[:x]
                    + "<a href="
                    + url
                    + ' target="_blank">'
                    + text
                    + "</a>"
                    + s[y:]
                )

        # 图像链接
        pattern = re.compile(r"!\[(.*)\]\((.*)\)")
        match = pattern.finditer(s)
        for a in match:
            if a:
                text, url = a.group(1, 2)
                x, y = a.span()
                s = s[:x] + "<img src=" + url + ' target="_blank">' + "</a>" + s[y:]

        # 角标
        pattern = re.compile(r"(.)\^\[([^\]]*)\]")
        match = pattern.finditer(s)
        k = 0
        for a in match:
            if a:
                sym, index = a.group(1, 2)
                x, y = a.span()
                s = s[: x + 8 * k] + sym + "<sup>" + index + "</sup>" + s[y + 8 * k :]
            k += 1

        return s


main()
