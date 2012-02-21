// Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This software is licensed under the terms of either the
// MIT License or the GNU Affero General Public License (AGPL) Version 3.
// http://www.c-tanzer.at/license/mit_or_agpl.html
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/L.js
//
// Purpose
//    Provide a function `L` to define a HTML element with a minimum of fuss
//
// Revision Dates
//    21-Feb-2012 (CT) Creation
//    ��revision-date�����
//--

"use strict";

( function (doc, undefined) {
    var assign_map =
        { innerHTML         : true
        , textContent       : true
        };
    var bool_map =
        { checked           : true
        , defer             : true
        , disabled          : true
        , multiple          : true
        , readonly          : true
        , selected          : true
        };
    var name_map =
        { "access_key"      : "accesskey"
        , className         : "class"
        , class_name        : "class"
        , html_for          : "for"
        , html              : "innerHTML"
        , inner_html        : "innerHTML"
        , max_length        : "maxLength"
        , read_only         : "readonly"
        , tab_index         : "tabindex"
        , text              : "textContent"
        , xml_lang          : "xml:lang"
        , xml_space         : "xml:space"
        };
    var tag_sep = /([#.])/;
    var add = function add (elem, children) {
        for (var i = 0, li = children.length, child; i < li; i++) {
            child = children [i];
            if (child) {
                if (child.constructor === Array) {
                    add (elem, child);
                } else {
                    if (typeof child === "string") {
                        child = doc.createTextNode (child);
                    };
                    elem.appendChild (child);
                };
            };
        };
    };
    var set = function set (elem, name, value) {
        var v;
        if (name in name_map) {
            name = name_map [name];
        };
        name = name.replace (/-/g, "_");
        if (value == null) {
            elem.removeAttribute (name);
        } else {
            v = name in bool_map ? !! value : "" + value;
            if (name in assign_map) {
                elem [name] = v;
            } else {
                elem.setAttribute (name, v);
            };
        };
    };
    var make = function make (tag, spec) {
        var children = Array.prototype.slice.call (arguments, 2);
        var classes  = [];
        var name, result, tps;
        if (! spec) {
            spec = {};
        };
        tps = tag.split (tag_sep);
        tag = tps [0];
        for (var i = 2, li = tps.length, p; i < li; i += 2) {
            p = tps [i];
            if (tps [i-1] === "#") {
                spec.id = p;
            } else {
                classes.push (p);
            };
        };
        if (classes.length) {
            spec.className = classes.join (" ");
        };
        result = doc.createElement (tag);
        for (name in spec) {
            if (spec.hasOwnProperty (name)) {
                set (result, name, spec [name]);
            };
        };
        if (children) {
            add (result, children);
        };
        result.$ =
            { add : add
            , set : set
            };
        return result;
    };
    $GTW.L = make;
  } (document)
);

// __END__ GTW/L.js
