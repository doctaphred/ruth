#!/usr/bin/env ruby
require 'json'
require 'liquid'


def render_liquid(template_string, context_string)
    template = Liquid::Template.parse(template_string, :error_mode => :strict)
    context = JSON.parse(context_string)
    return template.render(context, { strict_variables: true, strict_filters: true })
end


if __FILE__ == $0
    print render_liquid(ARGV[0], ARGV[1])
end


# TODO: reuse processes via pipes, Sinatra, or xml-rpc
# https://ruby-doc.org/stdlib-2.3.1/libdoc/xmlrpc/rdoc/XMLRPC/Client.html
# (or just stick it in AWS Lambda)
