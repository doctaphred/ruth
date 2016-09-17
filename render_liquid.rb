#!/usr/bin/env ruby
require 'json'
require 'liquid'


def render_liquid
    template = Liquid::Template.parse(ARGV[0], :error_mode => :strict)
    context = JSON.parse(ARGV[1])
    return template.render(JSON.parse(ARGV[1]), { strict_variables: true, strict_filters: true })
end


if __FILE__ == $0
    print render_liquid()
end


# TODO: reuse processes via pipes, Sinatra, or xml-rpc
# https://ruby-doc.org/stdlib-2.3.1/libdoc/xmlrpc/rdoc/XMLRPC/Client.html
# (or just stick it in AWS Lambda)
