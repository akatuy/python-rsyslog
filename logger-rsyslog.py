"""

rsyslog config: /etc/rsyslog.d/my-sample.conf:
$template AppLogFormat, "%TIMESTAMP:::date-pgsql%%TIMESTAMP:27:32:date-rfc3339%(%syslogseverity-text%)%msg%\n"
if $app-name == 'my-sample-app' then -/var/log/my-sample-app/app.log;AppLogFormat
& ~

"""

from __future__ import print_function
import argparse
import logging
import logging.handlers

APP_NAME = "my-sample-app"


def create_logger(app_name, log_level=logging.DEBUG, stdout=True, syslog=False, file=False):
    """
    create logging object with logging to syslog, file and stdout
    :param app_name app name
    :param log_level logging log level
    :param stdout log to stdout
    :param syslog log to syslog
    :param file log to file
    :return: logging object
    """
    # disable requests logging
    #logging.getLogger("requests").setLevel(logging.ERROR)
    #logging.getLogger("urllib3").setLevel(logging.ERROR)

    # create logger
    logger = logging.getLogger(app_name)
    logger.setLevel(log_level)

    # set log format to handlers
    formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')

    if file:
        # create file logger handler
        fh = logging.FileHandler('my-sample-app.log')
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    if syslog:
        # create syslog logger handler
        sh = logging.handlers.SysLogHandler(address='/dev/log')
        sh.setLevel(log_level)
        sf = logging.Formatter('%(name)s: %(message)s')
        sh.setFormatter(sf)
        logger.addHandler(sh)

    if stdout:
        # create stream logger handler
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


if __name__ == "__main__":
    print("BEGIN")

    parser = argparse.ArgumentParser(description='sample app with logging')
    parser.add_argument('-s', '--stdout', action='store_true', default=True, help='log to stdout')
    parser.add_argument('-r', '--rsyslog', action='store_true', default=False, help='log to syslog')
    parser.add_argument('-f', '--file', action='store_true', default=False, help='log file app.log')

    args = parser.parse_args()

    log = create_logger(
        app_name=APP_NAME,
        log_level=logging.DEBUG,
        syslog=args.rsyslog,
        stdout=args.stdout,
        file=args.file)

    log.debug("hello debug from my sample app")
    log.debug("hello error from my sample app")

    print("END")
