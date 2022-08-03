import time
import sys
import os

import psutil


class Prog:
    def __init__(
        self, iterations, track_time, stream, title, monitor, update_interval=None
    ):
        """ Initializes tracking object. """
        # 迭代次数计数
        self.cnt = 0
        self.title = title
        # 总迭代次数
        self.max_iter = iterations
        # bool 值，指示是否打印时间信息
        self.track = track_time
        self.start = time.time()
        self.end = None
        self.item_id = None
        # 保存预计剩余时间
        self.eta = None
        self.total_time = 0.0
        self.last_time = self.start
        # 是否使用 psutil 模块
        self.monitor = monitor
        # 存储将要使用的输出流
        self.stream = stream
        # 指示进度是否仍在计算中
        self.active = True
        # 定义输出方式
        self._stream_out = None
        # 定义缓冲刷新方式
        self._stream_flush = None
        # 输出流选择函数
        self._check_stream()
        self._print_title()
        # 进度更新的间隔
        self.update_interval = update_interval

        # monitor 为 True，表示决定使用 psutil 模块显示 cpu 和内存信息
        if monitor:
            self.process = psutil.Process()
        if self.track:
            self.eta = 1

    def update(self, iterations=1, item_id=None, force_flush=False):
        # 更新进度信息（进度条，进度百分比）
        """
        Updates the progress bar / percentage indicator.

        Parameters
        ----------
        iterations : int (default: 1)
            default argument can be changed to integer values
            >=1 in order to update the progress indicators more than once
            per iteration.
        item_id : str (default: None)
            Print an item_id sring behind the progress bar
        force_flush : bool (default: False)
            If True, flushes the progress indicator to the output screen
            in each iteration.

        """
        self.item_id = item_id
        # 更新计数
        self.cnt += iterations
        # 打印进度条
        self._print(force_flush=force_flush)
        # 确认是否完成，已完成则进行收尾工作
        self._finish()

    def _check_stream(self):
        # 确认使用哪个输出流
        """Determines which output stream (stdout, stderr, or custom) to use"""
        if self.stream:
            try:
                if self.stream == 1 and os.isatty(sys.stdout.fileno()):
                    self._stream_out = sys.stdout.write
                    self._stream_flush = sys.stdout.flush
                elif self.stream == 2 and os.isatty(sys.stderr.fileno()):
                    self._stream_out = sys.stderr.write
                    self._stream_flush = sys.stderr.flush
                # 当 self.stream 不为空，且 self.stream 具有 write 属性时
                elif self.stream is not None and hasattr(self.stream, "write"):
                    self._stream_out = self.stream.write
                    self._stream_flush = self.stream.flush
            except:
                print("Warning: No valid output stream.")

    def _elapsed(self):
        # 返回已花费时间
        """ Returns elapsed time at update. """
        # 将现在的时间赋值给 last_time
        self.last_time = time.time()
        # last_time - 开始时间 得出已花费时间
        return self.last_time - self.start

    def _calc_eta(self):
        # 计算预计完成剩余时间
        """ Calculates estimated time left until completion. """
        elapsed = self._elapsed()
        # 刚开始的时候，计算出的值不准，返回 None
        if self.cnt == 0 or elapsed < 0.001:
            return None
        rate = self.cnt / elapsed
        self.eta = (self.max_iter - self.cnt) / rate

    def _calc_percent(self):
        # 计算完成百分比
        """Calculates the rel. progress in percent with 2 decimal points."""
        return round(self.cnt / self.max_iter * 100, 2)

    def _get_time(self, _time):
        """获得格式化后的时间"""
        # 当时间小于 24 小时
        if _time < 86400:
            return time.strftime("%H:%M:%S", time.gmtime(_time))
        # 当时间大于 24 小时
        else:
            s = (
                str(int(_time // 3600))
                + ":"
                + time.strftime("%M:%S", time.gmtime(_time))
            )
            return s

    def _finish(self):
        # 确认是否已达到最大迭代次数（进度100%）
        """ Determines if maximum number of iterations (seed) is reached. """
        if self.cnt >= self.max_iter:
            # 将已花费时间复制给总花费时间 total_time
            self.total_time = self._elapsed()
            # 将现在时间赋值给结束时间 end
            self.end = time.time()
            # 为了强制刷新进度条，见 progbar 与 progpercent 类中的 _print()
            self.last_progress -= 1  # to force a refreshed _print()
            self._print()
            # 如果 self.track 为 True，表示需要显示时间信息
            if self.track:
                # 使用输出流打印格式化后的时间信息
                self._stream_out(
                    "\nTotal time elapsed: " + self._get_time(self.total_time)
                )
            self._stream_out("\n")
            # 进度计算已结束
            self.active = False

    def _print_title(self):
        # 打印标题
        """ Prints tracking title at initialization. """
        if self.title:
            self._stream_out("{}\n".format(self.title))
            self._stream_flush()

    def _print_eta(self):
        # 打印预计剩余时间
        """ Prints the estimated time left."""
        self._calc_eta()
        self._stream_out(" | ETA: " + self._get_time(self.eta))
        self._stream_flush()

    def _print_item_id(self):
        """ Prints an item id behind the tracking object."""
        self._stream_out(" | Item ID: %s" % self.item_id)
        self._stream_flush()

    def __repr__(self):
        str_start = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(self.start))
        str_end = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(self.end))
        # 刷新缓冲区
        self._stream_flush()

        time_info = (
            f"Title: {self.title}\n"
            f"  Started: {str_start}\n"
            f"  Finished: {str_end}\n"
            "  Total time elapsed: " + self._get_time(self.total_time)
        )
        if self.monitor:
            cpu_total = self.process.cpu_percent()
            mem_total = self.process.memory_percent()
            cpu_mem_info = f"  CPU: {cpu_total:.2f}%\n  Memory: {mem_total:.2f}%"

            return time_info + "\n" + cpu_mem_info

        return time_info
