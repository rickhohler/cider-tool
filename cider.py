import click
import plistlib
import subprocess
import os

"""
    MIT License

    Copyright (c) 2019 Rick Hohler

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

GREEN_CHECK = '\033[1;32;40m[✓]\033[0;37;40m'
YELLOW_CHECK = '\033[1;33;40m[!]\033[0;37;40m'
FAIL_DOT = '\033[1;31;40m✗\033[0;37;40m'
PASS_DOT = '\033[1;32;40m✗\033[0;37;40m'
IDENT = '    '

def replace_in_file(filename, orgstr, newstr):
    with open(filename) as f:
        newText=f.read().replace(orgstr, newstr)
    with open(filename, "w") as f:
        f.write(newText)

def dump_infoplist(bundle):
    info_filename = bundle + '/Info.plist'
    with open(info_filename, 'rb') as fp:
        info = plistlib.load(fp)
        props = info["ApplicationProperties"]
        print('ApplicationPath:    ' + props["ApplicationPath"])
        print('CFBundleIdentifier: ' + props["CFBundleIdentifier"])
        print('SigningIdentity:    ' + props["SigningIdentity"])
        print('Team:               ' + props["Team"])

def get_infoplist(info_filename):
    with open(info_filename, 'rb') as fp:
        return plistlib.load(fp)

@click.group()
def main():
    """
    Handy commands for iOS developers.
    """
    pass

@main.command()
@click.option('--bundle', help='Path to xcarchive bundle.')
def amend(bundle):
    """Set bundle properties."""
    if bundle and os.path.isdir(bundle):
        if bundle.endswith('.xcarchive'):
            amend_xcarchive(bundle)
    else:
        click.echo('Bundle was not found.')

def amend_xcarchive(bundle):
    info_filename = bundle + '/Info.plist'
    info = get_infoplist(info_filename)
    props = info["ApplicationProperties"]
    bundle_id = input('App Bundle Identifier [' + props["CFBundleIdentifier"] + ']: ')
    signing_identity = input('Signing Identity [' + props["SigningIdentity"] + ']: ')
    team_id = input('Apple Developer Team Id [' + props["Team"] + ']: ')
    if bundle_id:
        old_bid = props["CFBundleIdentifier"]
        replace_in_file(info_filename, old_bid, bundle_id)
        # Update bundle id in app bundle.
        app_path_info = bundle + '/' + props["ApplicationPath"] + '/Info.plist'
        replace_in_file(app_path_info, old_bid, bundle_id)
        print('+ Changed bundle identifier from \'' + props["CFBundleIdentifier"] + '\' to \'' + bundle_id + '\'')
    if signing_identity:
        replace_in_file(info_filename, props["SigningIdentity"], signing_identity)
        print('+ Changed signing identity from \'' + props["SigningIdentity"] + '\' to \'' + signing_identity + '\'')
    if team_id:
        replace_in_file(info_filename, props["Team"], team_id)
        print('+ Changed team id from \'' + props["Team"] + '\' to \'' + team_id + '\'')

@main.command()
@click.option('--bundle', help='Path to app bundle.')
def analyze(bundle):
    """Analyze iOS app bundle. Displays relevant information."""
    dump_infoplist(bundle)

@main.command()
@click.option('--verbose/--no-verbose', default=False, help='Verbose output.')
def doctor(verbose):
    """Show information about the installed tooling."""
    print('Doctor summary (to see all details, run doctor --verbose):')
    pro = subprocess.run(["which", "codesign", "/dev/null"], capture_output=True)
    if pro.returncode ==  1:
        print(GREEN_CHECK + ' Codesign tool installed')
        if verbose:
            print(IDENT + PASS_DOT + ' `which codesign`, exit 1')
    else:
        print(GREEN_CHECK + ' Codesign tool missing')
        if verbose:
            print(IDENT + FAIL_DOT + ' `which codesign`, exit ' + str(pro.returncode))
    pro = subprocess.run(["xcodebuild", "-version", "/dev/null"], capture_output=True)
    if pro.returncode == 0:
        xcinf = pro.stdout.decode('utf-8').split('\n')
        print(GREEN_CHECK + ' ' + xcinf[0] + ' (' + xcinf[1] + ') installed')
        if verbose:
            print(IDENT + PASS_DOT + ' `xcodebuild -version`, exit 0')
    else:
        print(GREEN_CHECK + ' Xcode missing')
        if verbose:
            print(IDENT + FAIL_DOT + ' `xcodebuild -version`, exit ' + str(pro.returncode))

    pro = subprocess.run(["/usr/bin/security", "-q", "find-certificate", "-a", "-c", "iPhone Developer:"], capture_output=True)
    if pro.returncode == 0:
        secout = pro.stdout.decode('utf-8').split('\n')
        raw_labls = list(filter(lambda s: 'labl' in s, secout))
        labls = set(list(map(lambda s: s[18:len(s)-1], raw_labls)))
        if len(labls) > 0:
            print(GREEN_CHECK + ' Keychain developer certifications')
            for _, val in enumerate(labls):
                print(IDENT + PASS_DOT + ' ' + val)
        else:
            print(GREEN_CHECK + ' Installed iOS developer certifications installed')
    else:
        print(GREEN_CHECK + ' List of keychain developer certifications failed')

    pro = subprocess.run(["/usr/bin/security", "-q", "find-certificate", "-a", "-c", "iPhone Distribution:"], capture_output=True)
    if pro.returncode == 0:
        secout = pro.stdout.decode('utf-8').split('\n')
        raw_labls = list(filter(lambda s: 'labl' in s, secout))
        labls = set(list(map(lambda s: s[18:len(s)-1], raw_labls)))
        if len(labls) > 0:
            print(GREEN_CHECK + ' Installed distribution certifications')
            for _, val in enumerate(labls):
                print(IDENT + PASS_DOT + ' ' + val)
        else:
            print(GREEN_CHECK + ' No iOS distribution certifications installed')
    else:
        print(GREEN_CHECK + ' List of keychain distribution certifications failed')

if __name__ == "__main__":
    main()
