Releasing procedure
===================

Prerelease
----------
Go to plone.app.locales directory::

    cd ~/svn/plonenext/3.3/src/plone.app.locales

Prepare the release::

    vi CHANGES.txt
    svn ci -m"Prepare release"

or::

    prerelease

Release
-------
Do the release::

    svn cp https://svn.plone.org/svn/plone/plone.app.locales/trunk https://svn.plone.org/svn/plone/plone.app.locales/tags/3.3.2 -m"Tagged, I'll tag externals on next commit"
    cd /tmp
    svn co https://svn.plone.org/svn/plone/plone.app.locales/tags/3.3.2

We have now to pin PloneTranslations.

First get the revision::

    cd 3.3.2/plone/app/locales/i18n
    svn info

And modify the externals accordingly::

    cd ..
    vi EXTERNALS.txt

You should have something like this::
    
    i18n -r88537 https://svn.plone.org/svn/collective/PloneTranslations/trunk/i18n
    locales -r88537 https://svn.plone.org/svn/collective/PloneTranslations/trunk/locales
    utils -r88537 https://svn.plone.org/svn/collective/PloneTranslations/trunk/utils

Set the svn:externals and commit::

    svn propset svn:externals -F EXTERNALS.txt .
    svn ci -m"Pinned revision of PloneTranslations"

    cd /tmp/3.3.2
    rm -rf plone/app/locales/i18n/kupu
    cd plone/app/locales/locales/ #Plone 3
    cd plone/app/locales/ # Plone 4
    for po in `find . -name "*.po"` ; do msgfmt -o `dirname $po`/`basename $po .po`.mo $po; done

    cd /tmp/3.3.2
    python setup.py mregister --strict sdist --formats=zip mupload

Update plone.app.locales version in versions.cfg and etc/versions in plonenext/3.3 and plonenext/3.2
For Plone4, it's in plone-coredev/branches/4.0.

Postrelease
-----------

Go back to trunk
Edit setup.py and CHANGES.txt ad commit::

    svn ci -m"Update version after release"

or::

    postrelease
