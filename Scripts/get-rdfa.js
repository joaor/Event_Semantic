main_div = document.getElementById("post-9");
result = "Stats:\nAbout: " + main_div.getAttribute("about");
result += "\nType: " + main_div.getAttribute("typeof");

divs = main_div.getElementsByTagName("div");
ps = divs[0].getElementsByTagName("p");

for (var i=0;i<ps.length;i=i+1) { 
	a = ps[i].getAttribute("rel");
	if (a != null) {
 		result += "\n\nRelation: " + a;
		b = ps[i].getElementsByTagName("span");
		for (var j=0;j<b.length;j=j+1) { 
			if (b[j].getAttribute("about") != null) {
				result += "\nAbout: " + b[j].getAttribute("about");
				result += "\nType: " + b[j].getAttribute("typeof");
			}
			if (b[j].getAttribute("property") != null) {
				result += "\nProperty: " + b[j].getAttribute("property");
				result += "\nValue: " + b[j].innerHTML;
			}
		}
	}
	else {
		b = ps[i].getElementsByTagName("span");
		for (var j=0;j<b.length;j=j+1) { 
			if (b[j].getAttribute("property") != null) {
				result += "\n\nProperty: " + b[j].getAttribute("property");
				result += "\nValue: " + b[j].innerHTML;
			}
		}
	}
}

alert(result);