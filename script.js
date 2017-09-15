(function() {
	"use strict";

	var locking = false;

	function $(ele) {
		return document.querySelector(ele);
	}

	function $$(ele) {
		return document.querySelectorAll(ele);
	}

	function ajax(url, callback) {
		var a = new XMLHttpRequest();
		a.open("GET", url);
		a.addEventListener("load", callback);
		a.send();
		return a;
	}

	window.addEventListener("load", function() {
		$("#lock").addEventListener("click", lock);
	});

	function lock(e) {
		if (!locking) {
			locking = true;
			ajax("api/setPercent?value=1", null);
			setTimeout(ajax, 1000, "api/setPercent?value=0", null);
			setTimeout(function() {
				locking = false;
			}, 1000);
		}
	}
})();
