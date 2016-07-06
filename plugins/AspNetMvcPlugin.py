#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
This is a sample plugin for ASP.NET MVC applications. 
It's not going to find everything!
"""
from re import compile
from random import randint

# Regex rule attempts to idenify classes denoted as a Controller
CONTRULE = "((\s:\s){1}(.)*Controller)"

def param_parse(params):
    """
    Function to parse and provide random values for parameters of ActionResults 
    Only handles certain builtin types within ASP.NET MVC!
    Returns a dictionary of parameter name and the "generated" value
    """
    results = {}
    for p in params.split(','):
        if '?' in p:
            p = p.replace('?', '')
        if 'bool' in p:
            pname = p.split('bool')[1]
            val = "false"
        elif 'sbyte' in p:
            pname = p.split('sbyte')[1]
            val = '123'
        elif 'int' in p:
            pname = p.split('int ')[1]
            val = randint(-2147483648, 2147483647)
        elif 'string' in p:
            pname = p.split('string ')[1]
            val = ""
        else:
            pname = p.split()[1]
            val = None
        if '=' in pname:
            pname = pname.split('=')[0].strip()
        pname = pname.strip()
        results[pname] = val

    return results

def run(filename):
    """
    MUST HAVE FUNCTION!
    Begins the plugin processing
    Returns a list of endpoints
    """
    run_results = []
    url = None
    cont = None
    # location isn't currently used
    location = ""
    prog = compile(CONTRULE)
    last_lines = []

    for line in filename:
        try:
            if prog.search(line):
                cont = line.split("Controller")[0].split("class ")[1]
            if cont:
                last_lines.append(line)
            if " ActionResult " in line and cont:
                params = line.split("(")[1].split(")")[0]
                action_point = line.split("ActionResult ")[1].split("(")[0]
                for prev_line in last_lines:
                    if "HttpPost" in prev_line:
                        http_meth = "POST"
                        break
                    else:
                        http_meth = "GET"
                if params:
                    p_string = "?"
                    for k, v in param_parse(params).items():
                        p_string += '%s=%s&' % (k, v)
                    url = "%s/%s/%s%s\t%s" % (location,
                                              cont, action_point,
                                              p_string[:-1], http_meth)
                else:
                    url = "%s/%s/%s\t%s" % (location, cont, action_point, http_meth)
                last_lines = []
            if url is not None:
                run_results.append(url)
                url = None
        except Exception as e:
            raise e
    return run_results

def get_name():
    # MUST HAVE FUNCTION! Returns plugin name.
    return "ASP.NET MVC"
