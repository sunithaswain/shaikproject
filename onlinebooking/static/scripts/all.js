/*hash functions used for rooting and redirection in script.js*/
;(function($) {
	$.hash = function() { return location.hash; };
	$.hash.getArr = function() { return getArr(); };
	$.hash.getL1 = function() { return getL1(); };
	$.hash.getL2 = function() { return getL2(); };
	$.hash.set = function(val) { set(val); };
	$.hash.setL1 = function(val) { setL1(val); };
	$.hash.setL2 = function(val) { setL2(val); };
	
	function set(val) {
		if(location.pathname!='/' && val.indexOf(location.pathname)>0) val = val.substring(val.indexOf(location.pathname)+location.pathname.length);
		location.hash = '/'+val+'/';
	}
	
	function setL1(val) {
		var arr = $.hash.getArr();
		if(arr.length>=1) {
			arr[0] = '/'+val+'/';
			location.hash = arr.join('#');
		} else {
			location.hash = '/'+val+'/';
		}
	}
	
	function setL2(val) {
		var arr = $.hash.getArr();
		if(val=='') $.hash.set($.hash.getL1());
		else if(arr.length>=2) {
			arr[1] = val;
			location.hash = arr.join('#');
		} else if(arr.length==1){
			arr.push(val);
			location.hash = arr.join('#');
		} else {
			location.hash = '/welcome/#'+val;
		}
	}
	
	function getL1() {
		var arr = $.hash.getArr();
		
		if(arr.length>=1) {
			if(arr[0].charAt(arr[0].length-1)=='/') arr[0]=arr[0].slice(0, -1);
			if(arr[0].charAt(0)=='/') arr[0]=arr[0].slice(1);
			return arr[0];
		}
		return null;
	}
	
	function getL2() {
		var arr = $.hash.getArr();
		if(arr.length>=2) return arr[1];
		return null;
	}
	
	function getArr() {
		
		var arr = $.hash().split('#');
		var retArr = new Array();
		$(arr).each(function(){
			if(this!='') retArr.push(this);
		});
		return retArr;
	}
})(jQuery);



/**
 * Cookie plugin
 *
 * Copyright (c) 2006 Klaus Hartl (stilbuero.de)
 * Dual licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 *
 */

/**
 * Create a cookie with the given name and value and other optional parameters.
 *
 * @example $.cookie('the_cookie', 'the_value');
 * @desc Set the value of a cookie.
 * @example $.cookie('the_cookie', 'the_value', { expires: 7, path: '/', domain: 'jquery.com', secure: true });
 * @desc Create a cookie with all available options.
 * @example $.cookie('the_cookie', 'the_value');
 * @desc Create a session cookie.
 * @example $.cookie('the_cookie', null);
 * @desc Delete a cookie by passing null as value. Keep in mind that you have to use the same path and domain
 *       used when the cookie was set.
 *
 * @param String name The name of the cookie.
 * @param String value The value of the cookie.
 * @param Object options An object literal containing key/value pairs to provide optional cookie attributes.
 * @option Number|Date expires Either an integer specifying the expiration date from now on in days or a Date object.
 *                             If a negative value is specified (e.g. a date in the past), the cookie will be deleted.
 *                             If set to null or omitted, the cookie will be a session cookie and will not be retained
 *                             when the the browser exits.
 * @option String path The value of the path atribute of the cookie (default: path of page that created the cookie).
 * @option String domain The value of the domain attribute of the cookie (default: domain of page that created the cookie).
 * @option Boolean secure If true, the secure attribute of the cookie will be set and the cookie transmission will
 *                        require a secure protocol (like HTTPS).
 * @type undefined
 *
 * @name $.cookie
 * @cat Plugins/Cookie
 * @author Klaus Hartl/klaus.hartl@stilbuero.de
 */

/**
 * Get the value of a cookie with the given name.
 *
 * @example $.cookie('the_cookie');
 * @desc Get the value of a cookie.
 *
 * @param String name The name of the cookie.
 * @return The value of the cookie.
 * @type String
 *
 * @name $.cookie
 * @cat Plugins/Cookie
 * @author Klaus Hartl/klaus.hartl@stilbuero.de
 */
jQuery.cookie = function(name, value, options) {
    if (typeof value != 'undefined') { // name and value given, set cookie
        options = options || {};
        if (value === null) {
            value = '';
            options.expires = -1;
        }
        var expires = '';
        if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
            var date;
            if (typeof options.expires == 'number') {
                date = new Date();
                date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
            } else {
                date = options.expires;
            }
            expires = '; expires=' + date.toUTCString(); // use expires attribute, max-age is not supported by IE
        }
        // CAUTION: Needed to parenthesize options.path and options.domain
        // in the following expressions, otherwise they evaluate to undefined
        // in the packed version for some reason...
        var path = options.path ? '; path=' + (options.path) : '';
        var domain = options.domain ? '; domain=' + (options.domain) : '';
        var secure = options.secure ? '; secure' : '';
        document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
    } else { // only name given, get cookie
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
};
