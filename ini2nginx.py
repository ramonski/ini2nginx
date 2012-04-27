# -*- coding: utf-8 -*-
#
# Writes Nginx Configs from an ini file.
#
# Usage: python ini2nginx.py -c nginx.ini -d configs/nginx
#
# You can extend the configs with your own config writer.

import os
import sys
import optparse
from StringIO import StringIO
import ConfigParser

# template, custom header and footer
TEMPLATE = open("template.cfg", "r").read()
HEADER = "### Nginx config for VHM %(server_name)s ###\n"
FOOTER = "# vim: set ft=nginx ts=4 sw=4 expandtab :"


# Pluggable Config Writers. Add your custom writers here
def example_writer(data):
    """ generates a nginx config

        @params {dict} data
            The parsed data of one section
    """
    name = data["server_name"]
    alias = data["server_alias"]
    data["name"] = " ".join([name, alias])
    data["x_hosting"] = name
    # XXX: hard coded upstream to allow different settings per configwriter,
    # e.g. to proxy_pass to varnish/pound etc.
    data["upstream"] = "http://localhost:8080"

    # generate config
    return TEMPLATE % data


# config writer plugins. Add custom writers here
CONFIG_WRITERS = [example_writer]


class Nginx(object):
    """ writes nginx configs out of an ini file
    """

    def __init__(self, config, out_directory):
        self.out_directory = out_directory
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(config)

    def __repr__(self):
        return "<%s @config: %s>" % (self.__class__.__name__, self.config)

    def get_sections(self):
        return self.config.sections()

    def get_options(self, section):
        return self.config.options(section)

    def get_items(self, section):
        return self.config.items(section)

    def write_file(self, filename, f):
        f_path = os.sep.join([self.out_directory, filename])
        config_file = open(f_path, "w")
        try:
            print "Writing Config %s -> %s" % (filename, f_path)
            config_file.write(f.getvalue())
        finally:
            config_file.close()

    def make_configs(self):
        """ writes all nginx configs
        """

        for section in self.get_sections():

            # get the data from the section
            data = dict(self.get_items(section))

            # generated nginx config
            nginx_config = StringIO()

            # write custom footer
            nginx_config.write(HEADER % data)

            for cw in CONFIG_WRITERS:
                if callable(cw):
                    # write a config
                    nginx_config.write(cw(data))

            # write custom footer
            nginx_config.write(FOOTER % data)

            # write to file
            filename = data.get("filename")
            self.write_file(filename, nginx_config)


if __name__ == "__main__":

    parser = optparse.OptionParser()

    parser.add_option('-c', '--config-file',
                      dest='config',
                      default='nginx.ini',
                      help='config ini file [default: %default]')

    parser.add_option('-d', '--directory',
                      dest='directory',
                      default='configs',
                      help='output directory [default: %default]')

    options, args = parser.parse_args(sys.argv)

    config = options.config
    out_directory = options.directory

    Nginx(config, out_directory).make_configs()

# vim: set ft=python ts=4 sw=4 expandtab :
