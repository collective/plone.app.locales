Releasing procedure
===================

Use a virtualenv with zest.releaser and zest.pocompile installed.

Go to plone.app.locales directory::

    cd src/plone.app.locales
    git pull

Verify there is no error in the po files::

    for po in `find . -name "*.po"` ; do msgfmt --no-hash -o `dirname $po`/`basename $po .po`.mo $po; done

Release::

    fullrelease
