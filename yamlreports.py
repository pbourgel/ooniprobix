# *****************************************************************************
# *                                                                           *
# * yamlreports.py                                                            *
# * Base parser and YAML file objects for OONIProbix                          *
# * Heavily modified from the example_parser.py script in the OONIProbe repo  *
# *                                                                           *
# * CONTAINS:                                                                 *
# * - Basic setup code to load and parse .yamloo files generated by OONIProbe *
# * - class YAMLReport: A YAML report representation                          *
# *                                                                           *
# *                                                                           *
# *****************************************************************************
import yaml
#import sys
#import wx
#import time

#Imports the Loader class that runs on libyaml in pure C, making things
#A LOT faster.
try:
    from yaml import CSafeLoader as Loader
except ImportError:
    print 'ImportError'
    from yaml import SafeLoader

#Written to close issue #12, this makes lists into a hashable type
#Taken from 
#https://github.com/scooby/yaml_examples/blob/master/handle_mappings.py
def construct_mapping_kludge(loader, node):
    """ This constructor painfully steps through the node and checks
that each key is hashable. Actually, what it does is checks
whether it knows how to *make* it hashable, and if so, does that.
If not it just lets it through and hopes for the best. But the
common problem cases are handled here. If you're constructing
objects directly from YAML, just make them immutable and hashable! """
    def anything(node):
        if isinstance(node, yaml.ScalarNode):
            return loader.construct_scalar(node)
        elif isinstance(node, yaml.SequenceNode):
            return loader.construct_sequence(node)
        elif isinstance(node, yaml.MappingNode):
            return construct_mapping_kludge(loader, node)
    def make_hashable(value):
        """ Reconstructs a non-hashable value. """
        if isinstance(value, list):
            return tuple(map(make_hashable, value))
        elif isinstance(value, set):
            return frozenset(value)
        elif isinstance(value, dict):
            return frozenset((make_hashable(key), make_hashable(val))
                             for key, val in value.items())
        else:
            return value
    def new_items():
        for k, v in node.value:
            yield (make_hashable(anything(k)), anything(v))
    return dict(new_items())
yaml.add_constructor(u'tag:yaml.org,2002:map', construct_mapping_kludge, 
                    Loader=Loader)

##Old code from very early versions of OONIProbix, kept for diagnostic purposes
#def walk_dict(dictionary,tabs):
#	ks = dictionary.keys()
#	for k in ks:
#		if type(dictionary[k]) is dict:
#			print '\t' * tabs + k
#			walk_dict(dictionary[k],tabs+1)
#		elif type(dictionary[k]) is list:
#			print '\t' * tabs + k
#			walk_list(dictionary[k],tabs+1)
#		else:
#			print '\t' * tabs + k
	
#def walk_list(lst,tabs):
#	for l in lst:
#		if type(l) is dict:
#			walk_dict(l,tabs+1)
#		elif type(l) is list:
#			walk_list(l,tabs+1)
#		else:
#			pass
#			if type(l) is str:
#				if len(l) < 50:
#					print '\t' * tabs + l
#			else:
#				print '\t' * tabs + l
				
# Representation of a YAML report
# Once constructed, it has the following fields
# report_name: the name of the .yamloo file it loaded
# report_header: The report header
# report_entries: A list of report entries
class YAMLReport():

    def __init__(self, filename):
#       i = 0
        f = open(filename,'r')
        yamloo = yaml.load_all(f, Loader=Loader)
        self.report_name = filename
        self.report_header = yamloo.next()
        self.report_entries = []
                
        for entry in yamloo:
            self.report_entries.append(entry)
#           i=i+1
        f.close()
