/*;Date.prototype.toString=function(){return isNaN (this) ? 'NaN' : [this.getFullYear(), this.getMonth() > 8 ? this.getMonth() + 1 : '0' + (this.getMonth() + 1), this.getDate() > 9 ? this.getDate() : '0' + this.getDate()].join('-');};
$.blockUI.defaults.message = '<p style="font-size:1.2em;margin:.5em 0;">'+textPleaseWait+'</p><p style="margin-top:0px;margin-bottom:.5em;"><img src="'+loadingImgUrl+'"/></p>';
$.blockUI.defaults.onBlock = function(){$.blockUI.defaults.blocked=true;};
$.blockUI.defaults.onUnblock = function(){$.blockUI.defaults.blocked=false;};
//$.datepicker.setDefaults({showOn:'both', buttonImage:indexUrl+'styles/images/calendar.gif', buttonImageOnly:true, dateFormat:defaultDateFormat, showOtherMonths:true, selectOtherMonths:true, minDate:0, showAnim:'', firstDay:0, gotoCurrent:true});*/




// Google analytics - code used with dc.js 
//var _gaq = _gaq || [];
//_gaq.push(['_setAccount', account], ['_setAllowLinker', true], ['_setDomainName', domainName]);
//_gaq.push(['_setReferrerOverride', referrerOverride]);
//_gaq.push(['_setCustomVar', 1, 'language', languageCode, 2]);
//if(referrerOverride!='') _gaq.push(['_setReferrerOverride', referrerOverride]);

//Google analytics - code used with analytics.js (Universal Analytics)


(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', account, 'auto');
//ga('send', 'pageview');

//End Google analytics - code used with analytics.js (Universal Analytics)



var offsetTop = null, pageTracker = null;

function toggleAddToCart() {/*must be present and empty*/}

function updateBreadCrumb(val) {
	var originalVal = val;
	var productItems = $('#product-items');
	var breadcrumb = $('<ul></ul>');
	
	val = val.replace('/results/return', '');
	val = val.replace('/results', '');
	
	if(val!='' && val!='welcome' && val!='cart' && val!='travellers' && val!='thank-you' && val!='404') {
		var el = $('a[href="'+val+'"]', productItems);
		if(el.html()==null) return;
		var parent = el.parent().parent().parent();
		var i = 3;
		while(parent.attr('id')!='product-items' && (i--)>0) {
			breadcrumb.prepend('<li>'+el.html()+'</li>');
			parent = el.parent().parent().parent();
			el = $('a:first', parent);
		}
		if(originalVal.indexOf('/results') != -1) breadcrumb.append('<li>'+labelResults+'</li>');
		if(originalVal.indexOf('/return') != -1) breadcrumb.append('<li>'+labelReturnTicket+'</li>');
	} 
	else if(val=='cart') breadcrumb.prepend('<li>'+labelCart+'</li>');
	else if(val=='travellers') breadcrumb.prepend('<li>'+labelcheckout+'</li>');
	else if(val=='thank-you') breadcrumb.prepend('<li>'+labelthankYou+'</li>');
	else if(val=='404') breadcrumb.prepend('<li>'+label404+'</li>');
	else breadcrumb.prepend('<li>'+labelHome+'</li>');
	
	$('#breadcrumb').html(breadcrumb.html());
	$('#breadcrumb li:last').addClass('last');
	
	if(pageTracker) {
		var trackPageview = '';
		$('#breadcrumb li').each(function(){trackPageview = trackPageview+'/'+$(this).text();});
		//trackPageview = trackPageview.replace(/ /g, "_");
		pageTracker._trackPageview(trackPageview);
	}
}

function replaceUnicode(s) {
	return s.replace(String.fromCharCode(223), 'ss').replace(String.fromCharCode(224), 'a').replace(String.fromCharCode(225), 'a').replace(String.fromCharCode(226), 'a').replace(String.fromCharCode(227), 'a').replace(String.fromCharCode(228), 'a').replace(String.fromCharCode(229), 'a').replace(String.fromCharCode(230), 'ae').replace(String.fromCharCode(231), 'c').replace(String.fromCharCode(232), 'e').replace(String.fromCharCode(233), 'e').replace(String.fromCharCode(234), 'e').replace(String.fromCharCode(235), 'e').replace(String.fromCharCode(236), 'i').replace(String.fromCharCode(237), 'i').replace(String.fromCharCode(238), 'i').replace(String.fromCharCode(239), 'i').replace(String.fromCharCode(241), 'n').replace(String.fromCharCode(242), 'o').replace(String.fromCharCode(243), 'o').replace(String.fromCharCode(244), 'o').replace(String.fromCharCode(246), 'o').replace(String.fromCharCode(249), 'u').replace(String.fromCharCode(250), 'u').replace(String.fromCharCode(251), 'u').replace(String.fromCharCode(252), 'u').replace(String.fromCharCode(255), 'y').replace(String.fromCharCode(339), 'oe');
}

$(function() {
	
	// Fix for kanpai whitelabel
	if (($.hash.getL1()== null) && (domainName == ".kanpai.fr")){
		$.hash.setL1('pass/jr_east_pass');
	}
	
	// Fix for Kyushu whitelabel
	if (($.hash.getL1()== null) && (domainName == ".jrkyushurailpass.com")){
		$.hash.setL1('pass/kyushu_rail_pass');
	}
	
	// Fix for WestJapanrail whitelabel
	if (($.hash.getL1()== null) && (domainName == ".westjapanrail.com")){
		$.hash.setL1('pass/hokuriku_arch_pass');
	}
	
	// Redirection for SJ whitelabel microsite
	
	if (($.hash.getL1()== null) && (window.location.href.toLowerCase().indexOf("thank-you") < 0) && (domainName == ".sj.se")){
		if (history.pushState) {
		    var newurl = window.location.protocol + "//" + window.location.host +'/rail/';
		    window.history.pushState({path:newurl},'',newurl);
		    location="/rail/?lang=sv";
		}
	}
	
	// Redirection for GulfAir whitelabel microsite
	
	if (($.hash.getL1()== null) && (window.location.href.toLowerCase().indexOf("thank-you") < 0) && (domainName == ".gulfair.com")){
		if (history.pushState) {
		    var newurl = window.location.protocol + "//" + window.location.host +'/rail/';
		    window.history.pushState({path:newurl},'',newurl);
		    location="/rail/";
		}
	}
	
	// Redirection for Eastjapanrail whitelabel 
	
	if (($.hash.getL1()== null) && (window.location.href.toLowerCase().indexOf("thank-you") < 0) && (domainName == ".eastjapanrail.com")){
		if (history.pushState) {
		    
		    var newurl = window.location.protocol + "//www.eastjapanrail.com";
		 
		    window.location.href=newurl;
		}
	}
	
	
    // Redirection for travelpass.scotrail.co.uk whitelabel 
	
	if (($.hash.getL1()== null) && (window.location.href.toLowerCase().indexOf("thank-you") < 0) && (domainName == ".scotrail.co.uk")){
		if (history.pushState) {
		    
		    //var newurl = window.location.protocol + "//www.scotrail.co.uk";
			var newurl = "https://www.scotrail.co.uk/tickets/combined-tickets-travel-passes";
		 
		    window.location.href=newurl;
		}
	}
	
	
	
	if(pageTracker && analyticsCode!='') {
		if(domainName=='.acprail.com' && document.referrer.split('?', 1)[0].indexOf('acprail.com')<0) $.cookie('realreferrer', document.referrer, {path:'/', domain:'acprail.com'});
		// Google analytics - code used with dc.js, traditional analytics - We remove it because we use analytics.js now
		/*
		pageTracker = _gat._getTracker(analyticsCode);
		pageTracker._setReferrerOverride($.cookie('realreferrer'));
		pageTracker._setDomainName(domainName);
		*/
	}
	
	$(window).bind('hashchange', function() {
		//$.blockUI();
		
		var hashL1 = $.hash.getL1();
		if (hashL1 != null) $('#pleaseWaitDialog').modal('show');
		//alert(hashL1);
		var load = 'welcome';
		if(hashL1!=null && hashL1!='' && (checkoutUrl!=window.location.pathname || hashL1=='thank-you')) load = hashL1;
		//else if(checkoutUrl==window.location.pathname) {$.unblockUI();return;} //load = 'travellers';
		else if(checkoutUrl==window.location.pathname) {$('#pleaseWaitDialog').modal('hide');return;} //load = 'travellers';
		updateBreadCrumb(load);
		$('#content').load(load, function(responseText, textStatus, XMLHttpRequest){
			//if(XMLHttpRequest.status==404) $('#content').load('404', function(){$.unblockUI();});
			if(XMLHttpRequest.status==404) $('#content').load('404', function(){$('#pleaseWaitDialog').modal('hide');});
		});
		// Google analytics - code used with dc.js, traditional analytics - We remove it because we use analytics.js now
		/*
		_gaq.push(['_trackPageview', '/booking/'+load]);
		_gaq.push(['_setCustomVar', 1, 'language', languageCode, 3]);
		*/
		//With analytics.js 
		ga('send', 'pageview', '/booking/'+load); // Send tracking page 
		
		
		$(window).trigger('scroll');
	}).trigger('hashchange');
	
	var countryList = $('#options-navigation-select-country');
	var countryListItems = countryList.children('option').get();
	countryListItems.sort(function(a, b) {
		a = replaceUnicode($(a).text().toLowerCase());
		b = replaceUnicode($(b).text().toLowerCase());
		return (a < b) ? -1 : (a > b) ? 1 : 0;
	});
	$.each(countryListItems, function(idx, itm) { countryList.append(itm); });

	/*if(!($.browser.msie && parseInt($.browser.version)<8)) {
		$(window).scroll(function() {
			if(offsetTop==null) {
				offsetTop = $('#gutter-wrap').offset().top;
				$('#gutter-wrap').css({'position':'absolute', 'top':offsetTop+'px', 'left':'50%', 'margin-left':'-480px', 'z-index':'10'});
				$('#content-wrap').css({'margin-top':'48px'});
			}
			var scrollTop = parseInt($(document).scrollTop());
			if(scrollTop<offsetTop) $('#gutter-wrap').css({'position':'absolute', 'top':offsetTop+'px'});
			else $('#gutter-wrap').css({'position':'fixed', 'top':'0px'});
		});
	}*/
});

function convertFrenchStr(source) {
    var A_regexp = /[\u00C0|\u00C1|\u00C2|\u00C3|\u00C4|\u00C5|\u00C6]/gi;
    var E_regexp = /[\u00C8|\u00C9|\u00CA|\u00CB]/gi;
    var I_regexp = /[\u00CC|\u00CD|\u00CE|\u00CF]/gi;
    var O_regexp = /[\u00D2|\u00D3|\u00D4|\u00D5|\u00D6|\u00D8]/gi;
    var U_regexp = /[\u00D9|\u00DA|\u00DB|\u00DC]/gi;
    var C_regexp = /[\u00C7]/gi;
    var Y_regexp = /[\u00FF]/gi;
    
    source = source.replace(A_regexp, 'a');
    source = source.replace(E_regexp, 'e');
    source = source.replace(I_regexp, 'i');
    source = source.replace(O_regexp, 'o');
    source = source.replace(U_regexp, 'u');
    source = source.replace(C_regexp, 'c');
    source = source.replace(Y_regexp, 'y');
    
    return source;
}




