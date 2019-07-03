/* SrollUp Button */
function scrollup() {
    var scrollup = document.getElementById('scrollup');
    var pageY = window.pageYOffset || document.documentElement.scrollTop;
    if (pageY >= 300) {
        scrollup.style.cssText = "visibility: visible";
        scrollup.style.opacity = "0.5";
    } else {
        scrollup.style.cssText = "visibility: hidden";
        scrollup.style.opacity = "0";
    }
}

function showDesigner() {
    var authorbox = document.getElementById('authorbox');
    var h1 = authorbox.getElementsByTagName('h1')[0];
    var h2 = authorbox.getElementsByTagName('h2')[0];
    var p = authorbox.getElementsByTagName('p')[0];
    authorbox.style.display = 'block';
    authorbox.classList.add("animation-slide-bottom");
    h2.classList.add("animation-fade");
    h2.classList.add("animation-delay-2");
    h1.classList.add("animation-fade");
    h1.classList.add("animation-delay-5");
    p.classList.add("animation-fade");
    p.classList.add("animation-delay-7");
    authorbox.onclick = function() {
        this.style.display = 'none';
        authorbox.classList.toggle("animation-slide-bottom");
    }
}
window.onscroll = function() {
    scrollup();
};
document.onkeydown = function(e) {
    e = e || event;
    if (e.ctrlKey && e.keyCode == 65) { // escape
        showDesigner();
        return false;
    }
};
/*tabs*/
var tabLinks = new Array();
var contentDivs = new Array();

function init() {
    // Grab the tab links and content divs from the page
    var tabListItems = document.getElementById('tabs').getElementsByTagName('a');
    console.log(tabListItems);
    for (var i = 0; i < tabListItems.length; i++) {
        var tabLink = tabListItems[i];
        var id = getHash(tabLink.getAttribute('href'));
        tabLinks[id] = tabLink;
        contentDivs[id] = document.getElementById(id);
    }
    // Assign onclick events to the tab links, and
    // highlight the first tab
    var i = 0;
    for (var id in tabLinks) {
        tabLinks[id].onclick = showTab;
        tabLinks[id].onfocus = function() {
            this.blur()
        };
        if (i == 0) tabLinks[id].className = 'button_default selected';
        i++;
    }
    // Hide all content divs except the first
    var i = 0;
    for (var id in contentDivs) {
        if (i != 0) contentDivs[id].className = 'tabContent hide';
        i++;
    }
}

function showTab() {
    var selectedId = getHash(this.getAttribute('href'));
    // Highlight the selected tab, and dim all others.
    // Also show the selected content div, and hide all others.
    for (var id in contentDivs) {
        if (id == selectedId) {
            tabLinks[id].className = 'button_default selected';
            contentDivs[id].className = 'tabContent';
        } else {
            tabLinks[id].className = 'button_default';
            contentDivs[id].className = 'tabContent animation-fade hide';
            
          
            //change link DayOfWeek buttons
            var dow = document.getElementById('dayOfWeek');
            var buttons = dow.getElementsByTagName('a');
            for (var i = 0; i < buttons.length; i++){
                var button = buttons[i];
                if (button.className == 'button_primary'){
                    //is not download button
                    var href = button.getAttribute('href');
                    console.log(button.className);
                    button.setAttribute('href', '#' + selectedId + '-' + href.slice(-3));
                }
               
            }


        }
        
    }
    // Stop the browser following the link
    return false;
}

function getFirstChildWithTagName(element, tagName) {
    for (var i = 0; i < element.childNodes.length; i++) {
        if (element.childNodes[i].nodeName == tagName) return element.childNodes[i];
    }
}

function getHash(url) {
    var hashPos = url.lastIndexOf('#');
    return url.substring(hashPos + 1);
};

function addEvent(obj, evnt, fn) {
    if (obj.addEventListener) {
        obj.addEventListener(evnt, fn, false);
    } else {
        obj["e" + evnt + fn] = fn;
        obj[evnt + fn] = function() {
            obj["e" + evnt + fn](window.event);
        }
        obj.attachEvent("on" + evnt, obj[evnt + fn]);
    }
};
//удаление события
function removeEvent(obj, evnt, fn) {
    if (obj.removeEventListener) {
        obj.removeEventListener(evnt, fn, false);
    } else {
        obj.detachEvent("on" + evnt, obj[evnt + fn]);
        obj[evnt + fn] = null;
        obj["e" + evnt + fn] = null;
    }
};
document.addEventListener("DOMContentLoaded", function(event) {
    var menuItems = document.querySelectorAll(".menustring_item");
    for (var i = 0; i < menuItems.length; i++) {
        menuItems[i].addEventListener('click', function() {
            var href = this.querySelector('.menustring_item_a').getAttribute('href');
            window.location.href = href;
        });
    }
});