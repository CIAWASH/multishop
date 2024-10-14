import ghasedakpack


sms = ghasedakpack.Ghasedak('fe2360610ce83f4bb3cebb1784e4ace4b694e80a2ae0e76634adcdaf558f27b3V5jW8SCKAHT3LQDh')
sms.verification({'receptor': '09385268660', 'type': '1', 'template': 'randcode', 'param1': '1234', 'param2': 'hi'})