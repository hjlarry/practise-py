# %%
import logging

LOG_FILENAME = "logging_example.out"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logging.debug("this msg should goto the log file")
with open(LOG_FILENAME, "rt") as f:
    body = f.read()
print("File:", body)
# %%
import glob
LOG_FILENAME = "logging_rotatingfile_example.out"
my_logger = logging.getLogger("MyLogger")
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20, backupCount=5)
my_logger.addHandler(handler)

for i in range(100):
    my_logger.debug("i=%d" % i)

logfiles = glob.glob('%s*'%LOG_FILENAME)
for filename in sorted(logfiles):
    print(filename)

# %%
logging.basicConfig(level=logging.WARNING)
logger1 = logging.getLogger('package1.module1')
logger2 = logging.getLogger('package2.module2')
logger1.warning('this msg comes from one module')
logger2.warning('this msg comes from another module')

# %%
import warnings
logging.basicConfig(level=logging.INFO)
warnings.warn('this msg will not to log')
logging.captureWarnings(True)
warnings.warn('this msg go to log')
