"""
   Usage: rebuild-pot.py <product> <path to products dir>

   If you are lazy you can also use atct, atrbw etc. as shorthands and if you
   set your INSTANCE_HOME correctly it will automagically use the right version.

   So 'rebuilt-pot.py atrbw' is a valid shorthand.
"""

import os, sys, string
from utils import getLongProductName, getProductPath

try:
    import win32api
    WIN32 = True
except ImportError:
    WIN32 = False

__I18NDUDE = os.environ.get('I18NDUDE', 'i18ndude')
__INSTANCE_HOME = os.environ.get('INSTANCE_HOME', '')

def rebuild(product, folder=''):
    product = getLongProductName(product)

    pot = product + '.pot'
    manualpot = '%s-manual.pot' % product
    generatedpot = '%s-generated.pot' % product
    if '/' in product:
        product = product.split('/')[1]

    log = 'rebuild-%s-pot.log' % product
    domain = product

    os.chdir('..')
    os.chdir('i18n')

    if not os.path.isfile(manualpot):
        print 'Manual pot missing for the given product: %s.' % manualpot
        sys.exit(3)

    folder2 = ''
    if product == 'plone':
        packages = (
            'archetypes.kss',
            'plone.contentrules',
            'plone.fieldsets',
            'plone.i18n',
            'plone.locking',
            'plone.memoize',
            'plone.openid',
            'plone.portlets',
            'plone.portlet.collection',
            'plone.portlet.static',
            'plone.session',
            'plone.intelligenttext',
            'plone.app.contentmenu',
            'plone.app.content',
            'plone.app.contentrules',
            'plone.app.controlpanel',
            'plone.app.customerize',
            'plone.app.form',
            'plone.app.i18n',
            'plone.app.imaging',
            'plone.app.iterate',
            'plone.app.kss',
            'plone.app.layout',
            'plone.app.linkintegrity',
            'plone.app.portlets',
            'plone.app.redirector',
            'plone.app.users',
            'plone.app.viewletmanager',
            'plone.app.vocabularies',
            'plone.app.workflow',
            'plone.app.openid',
            'plonetheme.sunburst',
            'plonetheme.classic',
            'Products.Archetypes',
            'Products.CMFDiffTool',
            'Products.validation',
        )
        add_products = (
            'Archetypes',
            'CMFDiffTool',
        )

        src = os.path.join(__INSTANCE_HOME, 'src')
        for package in packages:
            p = os.path.join(src, package)
            if os.path.isdir(p):
                folder2 += ' %s' % p
        src = os.path.join(__INSTANCE_HOME, 'products')
        for prod in add_products:
            p = os.path.join(src, prod)
            if os.path.isdir(p):
                folder2 += ' %s' % p

    foldererror = False
    if not os.path.isdir(folder) and folder == '':
        folder = os.path.join(__INSTANCE_HOME, 'Products')
        if os.path.isdir(folder):
            folder = os.path.join(folder, getProductPath(product))
            if not os.path.isdir(folder):
                # Try the src folder instead
                base = os.path.basename(folder)
                src = os.path.join(__INSTANCE_HOME, 'src')
                package = os.path.join(src, 'Products.%s' % base)
                if os.path.isdir(package):
                    folder = package
                else:
                    foldererror = True
        else:
            foldererror = True
    else:
        foldererror = True

    if foldererror:
        print 'Directory (%s) could not be found.' % folder
        sys.exit(4)

    # Remove the original file
    if os.path.isfile(pot):
        os.remove(pot)

    print 'Using %s to build new pot.\n' % folder
    cmd = __I18NDUDE + (' rebuild-pot --pot %s --create %s --merge %s ') % (pot, domain, manualpot)
    if product == 'plone':
        cmd += '--merge2 %s ' % generatedpot
    if product == 'plone':
        ignores = ('rss_template.pt',
                   'metadata_edit_form.cpt',
                   'metadirectives.py',
                   'Discussion_Item.xml',
                  )
        cmd += '--exclude="%s" ' % ' '.join(ignores)
    if product.startswith('kupu'):
        ignores = ('mmbase',
                   'widgeteer',
                   'kupu_kjax_support.xml.pt',
                   'kupu_migration.xml.pt',
                  )
        cmd += '--exclude="%s" ' % ' '.join(ignores)
    if product == 'plone':
        cmd += '%s %s > %s 2>&1' % (folder, folder2, log)
        # For debugging
        # cmd += '%s %s' % (folder, folder2)
    else:
        cmd += '%s > %s 2>&1' % (folder, log)
    print 'Rebuilding to %s - this takes a while, logging to %s' % (pot, log)
    os.system(cmd)

def main():
    if len(sys.argv) < 2:
        print 'You have to specify an option.'
        sys.exit(1)

    if len(sys.argv) == 2:
        rebuild(sys.argv[1])
    else:
        rebuild(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
