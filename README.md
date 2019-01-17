# Cider Tool
Handy commands for iOS developers.

## Installation

```sh
pip3 install -r requirements.txt
```

## Commmands

### Analyze

```sh
$ python3 cider.py analyze --bundle <name of xcarchive>

```

```sh
$ python3 cider.py analyze --bundle "example.xcarchive"
ApplicationPath:    Applications/DemoApp.app
CFBundleIdentifier: com.acme.DemoApp
SigningIdentity:    iPhone Developer: John Doe (XXXXXXXXXX)
Team:               ZZYYXXWWUU
```

### Doctor

```sh
$ python3 cider.py doctor

```

```sh
$ python3 cider.py doctor
Doctor summary (to see all details, run doctor --verbose):
[✓] Codesign tool installed
[✓] Xcode 10.1 (Build version 10B61) installed
[✓] Keychain developer certifications
    ✗ iPhone Developer: john.doe@acme.com (XXXXXXXXXX)
    ✗ iPhone Developer: jane.doe@acme.com (XXXXXXXXXX)
[✓] Installed distribution certifications
    ✗ iPhone Distribution: Acme Corporation (ZZYYXXWWUU)
```

### Amend

```sh
$ python3 cider.py doctor

```

```sh
$ python3 cider.py amend --bundle "example.xcarchive"
App Bundle Identifier [com.acme.DemoApp]: com.acme.NewDemoApp
Signing Identity [iPhone Developer: John Doe (ZZYYXXWWUU)]: iPhone Developer: Jane Doe (ZZYYXXWWUU)
Apple Developer Team Id [VVWWXXYYZZ]: ZZYYXXWWVV
+ Changed bundle identifier from 'com.acme.DemoAp to 'com.acme.NewDemoApp'
+ Changed signing identity from 'iPhone Developer: John Doe (ZZYYXXWWUU)' to 'iPhone Developer: Jane Doe (ZZYYXXWWUU)'
+ Changed team id from 'VVWWXXYYZZ' to 'ZZYYXXWWVV'
```

## License

- [MIT License][license-mit]
