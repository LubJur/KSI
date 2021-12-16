import time
from typing import NamedTuple, Optional, Dict, Tuple, List, Any
from collections import deque

from time import sleep
from bs4 import BeautifulSoup
import requests

class FullScrap(NamedTuple):
    # TUTO TRIDU ROZHODNE NEMEN
    linux_only_availability: List[str]
    most_visited_webpage: Tuple[int, str]
    changes: List[Tuple[int, str]]
    params: List[Tuple[int, str]]
    tea_party: Optional[str]

    def as_dict(self) -> Dict[str, Any]:
        return {
            'linux_only_availability': self.linux_only_availability,
            'most_visited_webpage': self.most_visited_webpage,
            'changes': self.changes,
            'params': self.params,
            'tea_party': self.tea_party
        }


def download_webpage(url: str, *args, **kwargs) -> requests.Response:
    """
    Download the page and returns its response by using requests.get
    :param url: url to download
    :return: requests Response
    """
    # TUTO FUNKCI ROZHODNE NEMEN
    print('GET ', url)
    return requests.get(url, *args, **kwargs)


def get_linux_only_availability(base_url: str) -> List[str]:
    """
    Finds all functions that area available only on Linux systems
    :param base_url: base url of the website
    :return: all function names that area available only on Linux systems
    """
    # Tuto funkci implementuj
    pass


def get_most_visited_webpage(base_url: str) -> Tuple[int, str]:
    """
    Finds the page with most links to it
    :param base_url: base url of the website
    :return: number of anchors to this page and its URL
    """
    # Tuto funkci implementuj
    # https://medium.com/analytics-vidhya/apply-depth-first-search-on-web-scraping-770ba20ba33f
    # na kazdu zo stranok by sme mohli dat request ci je aktivna a ak dostanem namiesto 200 spat kod pre cajovu kanvicu
    root = "https://python.iamroot.eu/"
    nodes_list = deque() # stack
    visited = set() # set
    nodes_list.append(root)
    visited.add(root)
    while len(nodes_list) > 0:
        node = nodes_list.pop()
        visited.add(node)
        #print(node)
        sleep(0.2)
        soup = BeautifulSoup(download_webpage(node).content, "html.parser")
        all_a = soup.find_all("a")
        for a in all_a:
            #print(a["href"])
            full = node + a["href"]
            #print(full)
            if full not in visited and a["href"][:6] != "https:" and a["href"][-1] != "#" and a["href"][-1] != "/":
                nodes_list.append(full[:-5] + "/")
    print("visited", visited)
    print("len visited", len(visited))
    """
    visited {'library/zipapp.html', 'tutorial/controlflow.html', 'c-api/codec.html', 'c-api/call.html', 'genindex-Z.html', 'select.html', 'asyncio-subprocess.html', 'library/json.html', 'plistlib.html', 'c-api/list.html', 'tkinter.ttk.html', 'library/python.html', 'library/audit_events.html', 'mailcap.html', 'custominterp.html', 'library/getopt.html', 'fractions.html', 'undoc.html', 'tkinter.html', 'platform.html', 'library/traceback.html', 'library/xml.sax.html', 'library/gzip.html', 'codecs.html', 'library/distutils.html', 'curses.html', 'tutorial/introduction.html', 'library/multiprocessing.shared_memory.html', 'reference/executionmodel.html', 'ftplib.html', 'operator.html', 'c-api/abstract.html', 'library/xml.html', 'email.encoders.html', 'library/weakref.html', 'library/decimal.html', 'c-api/datetime.html', '2.6.html', 'howto/logging.html', 'reference/expressions.html', 'genindex-J.html', 'library/contextlib.html', 'objbuffer.html', 'json.html', 'py_compile.html', 'c-api/index.html', 'library/logging.html', 'library/errno.html', 'howto/argparse.html', 'code.html', 'termios.html', 'c-api/capsule.html', 'nis.html', 'howto/descriptor.html', 'c-api/none.html', 'library/xmlrpc.server.html', 'cell.html', 'xmlrpc.server.html', 'library/asyncio-policy.html', 'library/binhex.html', 'library/secrets.html', 'tutorial/modules.html', 'arg.html', 'library/collections.html', 'library/code.html', 'library/pathlib.html', 'xml.etree.elementtree.html', 'library/unittest.html', 'asyncio-task.html', 'float.html', 'whatsnew/2.0.html', 'ast.html', 'library/asyncio-sync.html', 'urllib.error.html', '../using/editors.html', 'library/logging.handlers.html', 'library/doctest.html', 'library/ftplib.html', 'library/html.html', 'library/email.iterators.html', 'library/tkinter.html', 'library/cgi.html', 'concurrent.futures.html', 'locale.html', 'library/xdrlib.html', 'asyncio-future.html', 'library/types.html', 'library/xmlrpc.html', 'runpy.html', 'multiprocessing.shared_memory.html', 'c-api/apiabiversion.html', 'library/email.compat32-message.html', '3.1.html', '3.3.html', 'c-api/intro.html', 'library/winsound.html', 'library/poplib.html', 'codec.html', 'marshal.html', 'library/locale.html', 'library/frameworks.html', 'windows.html', 'library/modulefinder.html', 'allos.html', 'tutorial/appetite.html', 'library/posix.html', 'library/urllib.request.html', 'library/numbers.html', 'library/ctypes.html', 'email.charset.html', 'tutorial/venv.html', 'library/termios.html', 'library/urllib.error.html', 'unicodedata.html', 'email.generator.html', 'datetime.html', '../extending/embedding.html', 'faq/programming.html', 'library/lzma.html', 'logging.config.html', 'library/copy.html', 'constants.html', 'tkinter.dnd.html', 'library/pickletools.html', 'library/html.parser.html', 'asyncio-protocol.html', 'library/tkinter.font.html', 'cmdline.html', 'c-api/descriptor.html', 'extending/windows.html', 'asyncio-eventloop.html', 'library/timeit.html', 'pwd.html', 'list.html', 'whatsnew/3.2.html', 'library/formatter.html', 'library/hashlib.html', 'tkinter.tix.html', 'library/abc.html', 'genindex-A.html', 'contextlib.html', 'library/unittest.mock-examples.html', 'library/email.headerregistry.html', 'c-api/typeobj.html', 'uuid.html', 'gzip.html', 'library/sys.html', 'email.errors.html', 'asyncio-platforms.html', 'whatsnew/3.4.html', 'tracemalloc.html', 'library/pprint.html', 'tkinter.scrolledtext.html', 'library/binary.html', 'library/http.html', 'whatsnew/3.2.html#html', 'library/modules.html', 'object.html', 'library/xml.sax.handler.html', 'whatsnew/2.6.html', 'superseded.html', '/', 'library/netdata.html', 'debug.html', 'faq/installed.html', 'genindex-B.html', 'library/zoneinfo.html', 'sys.html', 'mapping.html', 'howto/instrumentation.html', 'library/reprlib.html', 'asynchat.html', 'whatsnew/3.1.html', 'c-api/memory.html', 'tutorial/datastructures.html', 'library/enum.html', 'structures.html', 'markup.html', 'c-api/typehints.html', 'library/venv.html', 'contents.html', '../contents.html', 'library/fnmatch.html', 'xml.sax.html', 'csv.html', 'c-api/sequence.html', 'library/socketserver.html', 'library/stdtypes.html', 'library/trace.html', 'library/xml.dom.minidom.html', 'library/unicodedata.html', 'xml.html', 'genindex-Q.html', 'pty.html', 'faq/gui.html', '3.0.html', 'library/email.contentmanager.html', 'faq/design.html', 'linecache.html', 'c-api/refcounting.html', 'binhex.html', 'email.html', 'library/concurrent.futures.html', 'descriptor.html', 'library/fileformats.html', 'library/asyncio-protocol.html', 'library/_thread.html', 'library/itertools.html', 'library/stringprep.html', 'c-api/unicode.html', 'html.parser.html', '../genindex.html', 'tkinter.messagebox.html', 'wave.html', 'netdata.html', 'library/language.html', 'library/telnetlib.html', 'array.html', 'library/binascii.html', 'library/asyncio-future.html', 'using/editors.html', 'reference/index.html', 'typehints.html', 'zipapp.html', 'distributing/index.html', '3.4.html', 'concurrency.html', 'clinic.html', 'sysconfig.html', 'library/importlib.metadata.html', 'pydoc.html', 'parser.html', 'library/keyword.html', 'c-api/stable.html', 'venv.html', 'complex.html', 'unittest.mock-examples.html', 'library/aifc.html', 'xdrlib.html', 'library/calendar.html', 'library/concurrency.html', 'library/archiving.html', 'reference/lexical_analysis.html', 'download.html', 'library/curses.panel.html', 'conversion.html', 'webbrowser.html', 'whatsnew/index.html', 'getopt.html', 'module.html', 'library/exceptions.html', 'apiabiversion.html', 'memory.html', 'xml.dom.html', 'c-api/iterator.html', 'embedding.html', 'library/shelve.html', 'library/grp.html', 'library/quopri.html', 'telnetlib.html', 'whatsnew/2.5.html', '../c-api/unicode.html', 'appetite.html', 'tutorial/interactive.html', 'library/email.message.html', 'c-api/objimpl.html', 'heapq.html', '../reference/index.html', 'unix.html', 'difflib.html', 'builtins.html', 'library/curses.ascii.html', 'nntplib.html', 'curses.panel.html', 'datastructures.html', 'archiving.html', 'readline.html', 'extending/embedding.html', 'copyreg.html', 'library/unix.html', 'library/email.header.html', 'stable.html', 'library/pydoc.html', 'library/array.html', 'whatsnew/3.4.html#html', 'bisect.html', 'email.message.html', '#cgitb.html', 'library/wave.html', 'c-api/method.html', 'c-api/import.html', 'library/2to3.html', 'library/builtins.html', 'library/xml.sax.utils.html', 'changelog.html', 'library/ipaddress.html', 'genindex-W.html', 'c-api/number.html', 'library/warnings.html', 'email.utils.html', 'library/linecache.html', 'inputoutput.html', 'subprocess.html', 'library/inspect.html', 'compound_stmts.html', 'gen.html', 'distribution.html', 'mailbox.html', 'shlex.html', 'email.compat32-message.html', 'library/signal.html', 'library/hmac.html', '2.3.html', 'xml.dom.pulldom.html', 'abstract.html', 'howto/ipaddress.html', 'howto/pyporting.html', 'binascii.html', 'os.path.html', 'tk.html', 'multiprocessing.html', 'mac.html', 'datatypes.html', 'struct.html', 'chunk.html', 'library/bdb.html', 'library/symbol.html', 'exceptions.html', 'faq/windows.html', 'license.html', 'genindex-Symbols.html', 'library/constants.html', 'frameworks.html', 'tutorial/stdlib2.html', 'library.html', 'examples.html', 'email.parser.html', 'library/importlib.html', 'library/nntplib.html', 'interpreter.html', 'tutorial/interpreter.html', '3.5.html', 'library/tkinter.colorchooser.html', 'reprlib.html', 'threading.html', 'graphlib.html', 'c-api/bytes.html', 'howto/sorting.html', 'file.html', 'c-api/reflection.html', 'logging.handlers.html', 'genindex-V.html', 'library/security_warnings.html', 'library/asyncio-platforms.html', 'formatter.html', 'imp.html', 'library/functools.html', 'urllib.request.html', 'library/__future__.html', 'library/graphlib.html', 'sorting.html', 'tutorial/errors.html', 'library/mm.html', 'keyword.html', 'zoneinfo.html', 'extending/index.html', '2.2.html', 'bytearray.html', 'genindex-P.html', 'library/pyclbr.html', 'c-api/gcsupport.html', 'library/syslog.html', 'token.html', 'configparser.html', 'howto/sockets.html', 'c-api/memoryview.html', 'library/index.html', 'pyclbr.html', 'concrete.html', 'library/pickle.html', '3.6.html', 'profile.html', '../howto/index.html', 'symtable.html', 'reference/simple_stmts.html', 'c-api/function.html', 'library/sunau.html', 'library/select.html', 'library/spwd.html', 'asyncio.html', 'ipaddress.html', 'library/ensurepip.html', 'tutorial/stdlib.html', 'site.html', 'library/profile.html', 'library/io.html', 'html.entities.html', 'c-api/float.html', 'executionmodel.html', 'library/urllib.parse.html', 'library/tarfile.html', 'library/asyncio-task.html', 'doctest.html', 'typing.html', 'installing/index.html', 'rlcompleter.html', 'curses.ascii.html', 'c-api/init_config.html', 'library/superseded.html', 'coro.html', 'library/cmd.html', 'library/filecmp.html', 'imaplib.html', 'extending/extending.html', 'library/functions.html', 'library/gc.html', 'tty.html', 'library/random.html', 'library/imp.html', 'setupscript.html', 'library/gettext.html', '3.9.html', 'msilib.html', 'c-api/complex.html', 'library/markup.html', 'library/pwd.html', 'library/xml.dom.html', 'slice.html', 'spwd.html', 'contextvars.html', 'fnmatch.html', 'importlib.metadata.html', 'bytes.html', 'library/http.cookies.html', 'library/devmode.html', 'library/persistence.html', '../reference/grammar.html', 'library/unittest.mock.html', 'secrets.html', '2to3.html', 'whatsnew/3.3.html', '../license.html', 'library/readline.html', 'fileinput.html', 'optparse.html', 'pyexpat.html', 'library/tkinter.messagebox.html', 'library/tracemalloc.html', 'library/asyncio-exceptions.html', 'library/bisect.html', 'library/fcntl.html', 'library/ssl.html', 'genindex-N.html', 'library/symtable.html', 'using/cmdline.html', 'urllib.parse.html', 'email.examples.html', '../bugs.html', 'shelve.html', 'whatsnew/3.5.html', 'reflection.html', 'introduction.html', 'library/asyncio-llapi-index.html', 'library/difflib.html', 'genindex-X.html', 'sourcedist.html', 'enum.html', 'calendar.html', 'modulefinder.html', 'whatsnew/3.7.html', 'function.html', 'library/email.mime.html', 'whatsnew/changelog.html', 'library/codecs.html', 'genindex-G.html', 'library/ast.html', 'audit_events.html', 'pprint.html', 'winreg.html', 'howto/urllib2.html', 'c-api/marshal.html', 'library/idle.html', 'filecmp.html', 'using/mac.html', 'tutorial/classes.html', '../py-modindex.html', 'tarfile.html', 'stdtypes.html', 'library/curses.html', 'sockets.html', 'timeit.html', 'tutorial/index.html', 'cgi.html', 'library/csv.html', 'html.html', 'text.html', 'faq/index.html', 'reference/compound_stmts.html', 'library/uuid.html', 'library/custominterp.html', 'library/html.html#module-html', 'howto/index.html', 'library/email.charset.html', 'whatsnew/3.8.html', 'library/audioop.html', 'instrumentation.html', 'stringprep.html', 'tutorial/floatingpoint.html', '../library/index.html', 'unicode.html', 'xml.sax.handler.html', 'pickletools.html', 'library/contextvars.html', 'library/re.html', 'sunau.html', 'glob.html', 'library/atexit.html', 'library/typing.html', 'gettext.html', 'weakref.html', 'library/datetime.html', 'smtplib.html', 'memoryview.html', 'ssl.html', 'library/concurrent.html', 'ctypes.html', 'library/netrc.html', 'library/compileall.html', 'library/glob.html', 're.html', 'genindex-H.html', 'cmath.html', 'library/smtplib.html', 'library/email.utils.html', 'c-api/cell.html', 'library/xmlrpc.client.html', 'dbm.html', 'init.html', 'whatsnew/2.4.html', 'library/runpy.html', 'genindex-C.html', 'expressions.html', 'library/dialog.html', 'zlib.html', 'c-api/sys.html', 'library/socket.html', 'trace.html', 'library/crypto.html', 'library/dataclasses.html', 'faulthandler.html', 'codeop.html', 'c-api/buffer.html', 'library/test.html', 'library/email.examples.html', 'library/crypt.html', '../glossary.html', 'library/zipimport.html', 'sched.html', 'apiref.html', 'library/ipc.html', 'argparse.html', 'poplib.html', 'about.html', 'library/allos.html', '__main__.html', 'library/zipfile.html', 'c-api/tuple.html', '../tutorial/index.html', 'library/intro.html', 'development.html', '../using/index.html', 'library/marshal.html', 'init_config.html', 'library/tk.html', 'typeobj.html', 'traceback.html', 'pathlib.html', 'stdlib2.html', 'genindex-Y.html', 'dis.html', 'math.html', 'misc.html', 'library/time.html', 'c-api/dict.html', 'library/operator.html', 'tempfile.html', 'library/rlcompleter.html', 'library/math.html', 'inspect.html', 'library/distribution.html', 'using/index.html', 'socketserver.html', 'asyncore.html', 'howto/clinic.html', 'library/asyncio.html', 'shutil.html', 'library/string.html', 'c-api/veryhigh.html', 'type.html', 'editors.html', 'numbers.html', 'tutorial/whatnow.html', 'whatsnew/3.3.html#html', 'signal.html', 'library/mailbox.html', 'number.html', 'stat.html', 'concurrent.html', 'library/email.policy.html', 'mm.html', 'library/dbm.html', 'extending/newtypes_tutorial.html', 'library/wsgiref.html', 'asyncio-llapi-index.html', 'aifc.html', 'tutorial/inputoutput.html', 'c-api/object.html', 'pdb.html', 'crypt.html', 'c-api/bytearray.html', 'library/os.path.html', 'cgitb.html', 'howto/logging-cookbook.html', 'importlib.html', 'mimetypes.html', 'email.headerregistry.html', 'library/mmap.html', 'c-api/structures.html', 'library/statistics.html', 'library/threading.html', 'extending/building.html', '#what-module-should-i-use-to-help-with-generating-html', 'search.html', 'grp.html', 'os.html', 'grammar.html', 'library/internet.html', 'test.html', 'errors.html', 'library/imghdr.html', 'asyncio-policy.html', 'sqlite3.html', 'veryhigh.html', 'library/functional.html', 'long.html', 'genindex-R.html', 'posix.html', 'collections.abc.html', 'library/datatypes.html', 'library/msvcrt.html', 'distutils/index.html', 'functions.html', 'library/pyexpat.html', 'configfile.html', 'modules.html', 'library/asynchat.html', 'persistence.html', 'urllib.html', 'c-api/concrete.html', '../c-api/index.html', 'fileformats.html', 'library/chunk.html', 'winsound.html', 'atexit.html', 'ipc.html', 'library/email.parser.html', 'library/queue.html', 'library/multiprocessing.html', '2.5.html', '3.8.html', 'c-api/arg.html', 'howto/unicode.html', 'library/collections.abc.html', 'xmlrpc.client.html', 'netrc.html', 'xml.sax.reader.html', 'library/tkinter.scrolledtext.html', 'ensurepip.html', 'sndhdr.html', '../faq/index.html', 'genindex-M.html', 'zipimport.html', 'faq/library.html', '../installing/index.html', 'appendix.html', 'functools.html', '../whatsnew/changelog.html', 'socket.html', 'library/i18n.html', 'tokenize.html', '__future__.html', 'idle.html', 'library/base64.html', 'asyncio-queue.html', 'genindex-O.html', 'programming.html', 'library/xml.etree.elementtree.html', 'library/platform.html', 'uu.html', 'allocation.html', 'sequence.html', 'dataclasses.html', 'builtdist.html', 'library/asyncio-queue.html', 'numeric.html', 'library/py_compile.html', 'cmd.html', 'hmac.html', 'library/http.cookiejar.html', '../library/html.html#module-html', 'library/logging.config.html', 'selectors.html', 'design.html', 'imghdr.html', 'textwrap.html', 'c-api/gen.html', 'c-api/set.html', 'bdb.html', 'c-api/mapping.html', 'library/xml.sax.reader.html', 'audioop.html', 'library/parser.html', 'queue.html', '2.1.html', 'internet.html', 'library/email.errors.html', 'whatnow.html', 'whatsnew/2.3.html', 'email.mime.html', 'utilities.html', 'distutils.html', 'library/heapq.html', 'copy.html', 'library/uu.html', 'genindex.html', 'c-api/utilities.html', 'newtypes_tutorial.html', 'library/imaplib.html', 'reference/grammar.html', 'urllib2.html', 'getpass.html', 'gc.html', 'library/numeric.html', 'bool.html', 'c-api/contextvars.html', 'library/pty.html', '2.0.html', 'collections.html', 'unittest.html', '3.7.html', 'hashlib.html', 'regex.html', 'pipes.html', 'tkinter.font.html', 'library/msilib.html', 'library/subprocess.html', 'library/cgitb.html#cgitb.html', 'gcsupport.html', 'genindex-L.html', 'using/windows.html', 'logging.html', 'library/html.entities.html', 'extending.html', 'c-api/coro.html', 'library/token.html', 'library/configparser.html', 'call.html', 'interactive.html', 'library/colorsys.html', 'pkgutil.html', 'whatsnew/2.7.html', 'library/selectors.html', 'library/smtpd.html', 'library/http.server.html', 'library/tkinter.ttk.html', 'c-api/type.html', 'c-api/long.html', 'compileall.html', '../copyright.html', 'general.html', 'whatsnew/2.1.html', 'mmap.html', 'library/site.html', 'library/bz2.html', 'library/textwrap.html', 'installed.html', 'library/windows.html', 'objimpl.html', 'email.iterators.html', 'email.policy.html', 'tutorial/appendix.html', 'genindex-I.html', 'lexical_analysis.html', 'urllib.robotparser.html', 'lzma.html', 'tabnanny.html', 'library/pkgutil.html', 'c-api/objbuffer.html', '3.2.html', 'c-api/allocation.html', 'library/asyncio-subprocess.html', 'c-api/conversion.html', 'library/sndhdr.html', 'library/argparse.html', 'types.html', '../tutorial/appendix.html', 'itertools.html', 'library/fractions.html', 'dialog.html', '../howto/instrumentation.html', 'whatsnew/3.6.html', 'library/mimetypes.html', 'time.html', 'syslog.html', 'classes.html', 'library/fileinput.html', 'gui.html', 'copyright.html', 'import.html', '../extending/index.html', 'library/webbrowser.html', 'email.header.html', 'library/dis.html', 'unittest.mock.html', 'library/tempfile.html', 'genindex-D.html', 'genindex-F.html', 'library/debug.html', 'genindex-U.html', 'whatsnew/3.9.html', 'c-api/code.html', 'py-modindex.html', 'c-api/file.html', 'dict.html', 'zipfile.html', 'library/asyncio-api-index.html', 'library/http.client.html', 'refcounting.html', 'library/text.html', 'bz2.html', '../index.html', 'faq/general.html', 'howto/curses.html', 'bugs.html', 'colorsys.html', 'howto/cporting.html', 'library/undoc.html', 'library/shlex.html', 'tuple.html', 'building.html', 'errno.html', 'floatingpoint.html', 'io.html', 'language.html', 'whatsnew/3.0.html', 'library/getpass.html', 'library/plistlib.html', 'library/nis.html', 'library/mailcap.html', 'pyporting.html', 'tkinter.colorchooser.html', 'library/winreg.html', 'library/stat.html', 'buffer.html', 'reference/datamodel.html', 'decimal.html', 'datamodel.html', 'howto/regex.html', 'library/zlib.html', 'wsgiref.html', 'library/asyncore.html', 'using/unix.html', 'functional.html', 'library/asyncio-stream.html', 'library/copyreg.html', 'devmode.html', 'fcntl.html', 'c-api/init.html', '#html', 'library/tkinter.dnd.html', 'quopri.html', 'c-api/iter.html', 'library/tabnanny.html', 'stdlib.html', 'asyncio-stream.html', 'genindex-all.html', 'genindex-K.html', 'library/optparse.html', 'reference/introduction.html', 'glossary.html', 'index.html', 'library/struct.html', 'asyncio-api-index.html', 'genindex-T.html', 'library/tty.html', 'c-api/slice.html', 'binary.html', 'xmlrpc.html', '_thread.html', 'library/xml.dom.pulldom.html', 'library/os.html', 'c-api/exceptions.html', 'intro.html', 'library/sched.html', 'library/filesys.html', 'set.html', 'msvcrt.html', 'email.contentmanager.html', 'library/shutil.html', 'capsule.html', 'abc.html', 'library/tokenize.html', 'library/email.encoders.html', 'library/urllib.robotparser.html', 'asyncio-exceptions.html', 'whatsnew/2.2.html', 'library/faulthandler.html', '../c-api/apiabiversion.html', 'string.html', 'c-api/module.html', 'library/sysconfig.html', 'python.html', 'asyncio-sync.html', 'c-api/weakref.html', 'none.html', 'library/pdb.html', '#module-html', 'resource.html', 'statistics.html', 'xml.sax.utils.html', 'library/ossaudiodev.html', 'i18n.html', 'smtpd.html', 'library/cmath.html', 'library/__main__.html', 'library/codeop.html', 'simple_stmts.html', 'pickle.html', 'faq/extending.html', 'reference/import.html', 'library/resource.html', 'library/tkinter.tix.html', 'library/email.generator.html', 'warnings.html', 'extending/newtypes.html', 'genindex-S.html', 'library/asyncio-eventloop.html', 'genindex-E.html', 'controlflow.html', 'security_warnings.html', 'library/sqlite3.html', 'logging-cookbook.html', 'cporting.html', 'library/email.html', 'library/cgitb.html', 'asyncio-dev.html', 'reference/toplevel_components.html', 'commandref.html', 'iterator.html', 'ossaudiodev.html', 'library/misc.html', 'method.html', 'turtle.html', 'c-api/bool.html', 'library/turtle.html', '2.4.html', 'library/urllib.html', 'crypto.html', 'library/asyncio-dev.html', 'toplevel_components.html', 'base64.html', 'xml.dom.minidom.html', '../distributing/index.html', 'symbol.html', '2.7.html', 'random.html', 'filesys.html', 'genindex-_.html', 'iter.html', 'library/pipes.html', 'library/development.html', 'howto/functional.html', '../library/security_warnings.html', 'newtypes.html'}
nodes_list deque([])
{"linux_only_availability": null, "most_visited_webpage": null, "changes": null, "params": null, "tea_party": null}
took 974 s
    soup = BeautifulSoup(download_webpage("https://python.iamroot.eu/").content, "html.parser")
    a_tags = soup.findAll("a")
    stack = []
    for a in a_tags:
        url = a.get("href")
        print(url)
        #if url[:4] != "http":
        if url not in stack:
            stack.append("https://python.iamroot.eu/" + url)

    print(stack)
    """

def get_changes(base_url: str) -> List[Tuple[int, str]]:
    """
    Locates all counts of changes of functions and groups them by version
    :param base_url: base url of the website
    :return: all counts of changes of functions and groups them by version, sorted from the most changes DESC
    """
    # Tuto funkci implementuj
    pass


def get_most_params(base_url: str) -> List[Tuple[int, str]]:
    """
    Finds the function that accepts more than 10 parameters
    :param base_url: base url of the website
    :return: number of parameters of this function and its name, sorted by the count DESC
    """
    # Tuto funkci implementuj
    pass


def find_secret_tea_party(base_url: str) -> Optional[str]:
    """
    Locates a secret Tea party
    :param base_url: base url of the website
    :return: url at which the secret tea party can be found
    """
    # Tuto funkci implementuj
    pass


def scrap_all(base_url: str) -> FullScrap:
    """
    Scrap all the information as efficiently as we can
    :param base_url: base url of the website
    :return: full web scrap of the Python docs
    """
    # Tuto funkci muzes menit, ale musi vracet vzdy tyto data
    scrap = FullScrap(
        linux_only_availability=get_linux_only_availability(base_url),
        most_visited_webpage=get_most_visited_webpage(base_url),
        changes=get_changes(base_url),
        params=get_most_params(base_url),
        tea_party=find_secret_tea_party(base_url)
    )
    return scrap


def main() -> None:
    """
    Do a full scrap and print the results
    :return:
    """
    # Tuto funkci klidne muzes zmenit podle svych preferenci :)
    import json
    time_start = time.time()
    print(json.dumps(scrap_all('https://python.iamroot.eu/').as_dict()))
    print('took', int(time.time() - time_start), 's')


if __name__ == '__main__':
    main()