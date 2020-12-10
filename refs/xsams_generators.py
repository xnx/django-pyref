from xml.sax.saxutils import escape
import datetime
import urllib.parse
from . import xsams_settings
from .xsams_utils import (make_xsams_id, make_mandatory_tag, make_optional_tag,
                          xsams_source_type)

XSAMS_VERSION = xsams_settings.XSAMS_VERSION
NODEID = xsams_settings.NODEID

def get_timestamp():
    return datetime.datetime.now().isoformat()

def xsams_preamble(timestamp=None):
    """
    The XML processing instruction and root element, specifying the XSAMS
    version and Schema location.
    Also outputs a comment line with the time of the query.

    """
    yield '<?xml version="1.0" encoding="UTF-8"?>\n'
    yield '<XSAMSData xmlns="http://vamdc.org/xml/xsams/%s"' % XSAMS_VERSION
    yield ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
    yield ' xmlns:cml="http://www.xml-cml.org/schema"'
    yield ' xsi:schemaLocation="http://vamdc.org/xml/xsams/%s %s">\n'\
            % (XSAMS_VERSION, xsams_settings.SCHEMA_LOCATION)
    if timestamp:
        # TODO convert no. of secs to date and time
        yield '<!-- TIMESTAMP: %s -->' % timestamp


def xsams_close():
    yield '</XSAMSData>'


def xsams_source(ref):
    """
    Yields the XML for an individual source in the XSAMS document.

    Arguments:
    ref: an instance of the Ref class.

    """

    yield '<Source sourceID="{}s">'.format(make_xsams_id('B', ref.id))
    if ref.note:
        yield '<Comments>%s</Comments>' % escape(ref.note)
    yield '<Authors>'
    for author in ref.authors_list:
        yield '<Author><Name>%s</Name></Author>' % author
    yield '</Authors>'
    yield make_mandatory_tag('Title', escape(ref.title), '[This source does'
                                        ' not have a title]')
    yield make_mandatory_tag('Category', xsams_source_type(ref.source_type),
                             '')
    # XXX what to do when the year is missing?
    yield make_mandatory_tag('Year', ref.year, '9999')
    yield make_optional_tag('SourceName', ref.journal)
    yield make_optional_tag('Volume', ref.volume)
    yield make_optional_tag('PageBegin', ref.page_start)
    yield make_optional_tag('PageEnd', ref.page_end)
    yield make_optional_tag('ArticleNumber', ref.article_number)
    yield make_optional_tag('UniformResourceIdentifier',
                    urllib.parse.quote(ref.url, safe='%:=/?~#+!$,;\'@()*'))
    yield make_optional_tag('DigitalObjectIdentifier', ref.doi)
    yield '</Source>\n'


def xsams_sources(sources):
    """
    Yields the XML for the sources in the XSAMS document.

    Arguments:
    sources: a list of sources to produce the XSAMS output for.

    """

    yield '<Sources>\n'
    for source in sources:
        yield from xsams_source(source)
    yield '</Sources>\n'


def xsams_molecular_chemical_species(species):
    """
    Yield the XML for the MolecularChemicalSpecies element describing the
    isotopologue iso.

    """

    molecule = iso.molecule
    yield '<MolecularChemicalSpecies>'
    yield make_referenced_text_tag('OrdinaryStructuralFormula', iso.iso_name,
         'An isotopologue of the molecule %s' % molecule.ordinary_formula, [])
    yield make_optional_tag('StoichiometricFormula',
                            molecule.stoichiometric_formula)
    # XXX hard-code the ion-charge for now:
    ion_charge = None
    if molecule.ordinary_formula == 'NO+':
        ion_charge = '1'
    yield make_optional_tag('IonCharge', ion_charge)
    yield make_referenced_text_tag('ChemicalName', molecule.common_name)
    yield make_optional_tag('InChI', iso.InChI)
    yield make_optional_tag('InChIKey', iso.InChIKey)

    # XXX hard-code partition function output for now:
    for chunk in make_partition_function_tag(iso):
        yield chunk

    yield make_optional_tag('MoleculeStructure',
                            get_molecule_cml_contents(iso.cml))
    yield '<StableMolecularProperties>'
    yield make_datatype_tag('MolecularWeight',iso.mass, 'amu')
    yield '</StableMolecularProperties>'
    yield '</MolecularChemicalSpecies>\n'


def xsams(refs):
    try:
        iter(refs)
    except TypeError:
        refs = [refs]

    timestamp = get_timestamp()
    yield from xsams_preamble(timestamp=timestamp)
    yield from xsams_sources(refs)
    yield from xsams_close()
