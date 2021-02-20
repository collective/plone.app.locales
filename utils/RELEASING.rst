Releasing procedure
===================

Use a virtualenv with zest.releaser and zest.pocompile installed.

Go to plone.app.locales directory::

    cd src/plone.app.locales
    git pull

Verify there is a changelog entry for each change, add any missing entries if necessary.

Verify there is no errors in the po files::

    for po in `find . -name "*.po"` ; do msgfmt --no-hash -o `dirname $po`/`basename $po .po`.mo $po; done

You can ignore the errors "'msgid' and 'msgstr' entries do not both end with '\n'". If there are other errors, please fix them.

Release::

    fullrelease

In the correct buildout.coredev branch, change the version of
"plone.app.locales" in versions.cfg, commit and push the change.
