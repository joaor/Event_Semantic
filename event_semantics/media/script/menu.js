	var timeBeforeAutoHide = 700;	// Microseconds to wait before auto hiding menu(1000 = 1 second)
	var slideSpeed_out = 10;	// Steps to move sub menu at a time ( higher = faster)
	var slideSpeed_in = 10;
		
	
	var slideTimeout_out = 25;	// Microseconds between slide steps ( lower = faster)
	var slideTimeout_in = 10;	// Microseconds between slide steps ( lower = faster)
	
	var showSubOnMouseOver = true;	// false = show sub menu on click, true = show sub menu on mouse over
	var fixedSubMenuWidth = false;	// Width of sub menu items - A number(width in pixels) or false when width should be dynamic
	
	var xOffsetSubMenu = 0; 	// Offset x-position of sub menu items - use negative value if you want the sub menu to overlap main menu
	
	var slideDirection = 'right';	// Slide to left or right ?
	
	/* Don't change anything below here */
	
	var activeSubMenuId = false;
	var activeMainMenuItem = false;
	var currentZIndex = 1000;		
	var autoHideTimer = 0;
	var submenuObjArray = new Array();
	var okToSlideInSub = new Array();
	var subPositioned = new Array();
	

	function stopAutoHide()
	{
		autoHideTimer = -1;
	}
	
	function initAutoHide()
	{
		autoHideTimer = 0;
		if(autoHideTimer>=0)autoHide();
	}
	
	function autoHide()
	{
		
		if(autoHideTimer>timeBeforeAutoHide)
		{
			
			if(activeMainMenuItem){
				activeMainMenuItem.className='';
				activeMainMenuItem = false;
			}
			
			if(activeSubMenuId){
				var obj = document.getElementById('subMenuDiv' + activeSubMenuId);
				showSub();
			}
		}else{
			if(autoHideTimer>=0){
				autoHideTimer+=50;
				setTimeout('autoHide()',50);
			}
		}
	}	
	
	function getTopPos(inputObj)
	{		
	  var returnValue = inputObj.offsetTop;
	  while((inputObj = inputObj.offsetParent) != null)returnValue += inputObj.offsetTop;
	  return returnValue;
	}
	
	function getLeftPos(inputObj)
	{
	  var returnValue = inputObj.offsetLeft;
	  while((inputObj = inputObj.offsetParent) != null)returnValue += inputObj.offsetLeft;
	  return returnValue;
	}
	
	function showSub()
	{
		var subObj = false;
		if(this && this.tagName){
			var numericId = this.parentNode.id.replace(/[^0-9]/g,'');
			okToSlideInSub[numericId] = false;
			var subObj = document.getElementById('subMenuDiv' + numericId);
			if(activeMainMenuItem)activeMainMenuItem.className='';
			if(subObj){
				if(!subPositioned[numericId]){
					if(slideDirection=='right'){
						subObj.style.left = getLeftPos(submenuObjArray[numericId]['parentDiv']) + submenuObjArray[numericId]['parentDiv'].offsetWidth + xOffsetSubMenu + 'px';
					}else{
						subObj.style.left = getLeftPos(submenuObjArray[numericId]['parentDiv']) + xOffsetSubMenu + 'px';
						
					}
					submenuObjArray[numericId]['left'] = subObj.style.left.replace(/[^0-9]/g,'');
					subObj.style.top = getTopPos(submenuObjArray[numericId]['parentDiv']) + 'px';
					subPositioned[numericId] = true;
				}				
				subObj.style.visibility = 'visible';
				subObj.style.zIndex = currentZIndex;
				currentZIndex++;	
				this.className='activeMainMenuItem';
				activeMainMenuItem = this;
			}
		}else{
			var numericId = activeSubMenuId;
		}
		if(activeSubMenuId && (numericId!=activeSubMenuId || !subObj))slideMenu(activeSubMenuId,(slideSpeed_in*-1));
		if(numericId!=activeSubMenuId && this && subObj){
			subObj.style.width = '0px';	
			slideMenu(numericId,slideSpeed_out);
			activeSubMenuId = numericId;
		}else{
			if(numericId!=activeSubMenuId)activeSubMenuId = false;
		}
		if(showSubOnMouseOver)stopAutoHide();
	}
	
	function slideMenu(menuIndex,speed){
		var obj = submenuObjArray[menuIndex]['divObj'];
		var obj2 = submenuObjArray[menuIndex]['ulObj'];
		var width = obj.offsetWidth + speed;
		if(speed<0){
			if(width<0)width = 0;
			obj.style.width = width + 'px';
			if(slideDirection=='left'){
				obj.style.left = submenuObjArray[menuIndex]['left'] - width + 'px';
				obj2.style.left = '0px';
			}else{
				obj2.style.left = width - submenuObjArray[menuIndex]['width'] + 'px' 
			}
			if(width>0 && okToSlideInSub[menuIndex])setTimeout('slideMenu(' + menuIndex + ',' + speed + ')',slideTimeout_in); else{
				obj.style.visibility = 'hidden';
				obj.style.width = '0px';
				if(activeSubMenuId==menuIndex)activeSubMenuId=false;
			}
			
		}else{
			if(width>submenuObjArray[menuIndex]['width'])width = submenuObjArray[menuIndex]['width'];
			if(slideDirection=='left'){
				obj.style.left = submenuObjArray[menuIndex]['left'] - width + 'px';
				obj2.style.left = '0px';
			}else{
				obj2.style.left = width - submenuObjArray[menuIndex]['width'] + 'px' 
			}		
			
			obj.style.width = width + 'px';
			if(width<submenuObjArray[menuIndex]['width']){
				setTimeout('slideMenu(' + menuIndex + ',' + speed + ')',slideTimeout_out);
			}else{
				okToSlideInSub[menuIndex] = true;
			}
		}
	}
	function resetPosition()
	{
		subPositioned.length = 0;
	}
			
	function initLeftMenu()
	{
		var menuObj = document.getElementById('dhtmlgoodies_menu');	
		var mainMenuItemArray = new Array();
		
		var mainMenuItem = menuObj.getElementsByTagName('LI')[0];
		while(mainMenuItem){
			if(mainMenuItem.tagName && mainMenuItem.tagName.toLowerCase()=='li'){
				mainMenuItemArray[mainMenuItemArray.length] = mainMenuItem;
				var aTag = mainMenuItem.getElementsByTagName('A')[0];
				if(showSubOnMouseOver)
					aTag.onmouseover = showSub;	
				else
					aTag.onclick = showSub;	
			}
			mainMenuItem = mainMenuItem.nextSibling;
		}		
		
		var lis = menuObj.getElementsByTagName('A');
		for(var no=0;no<lis.length;no++){
			if(!showSubOnMouseOver)lis[no].onmouseover = stopAutoHide;
			lis[no].onmouseout = initAutoHide;
			lis[no].onmousemove = stopAutoHide;
		}
				
		for(var no=0;no<mainMenuItemArray.length;no++){
			var sub = mainMenuItemArray[no].getElementsByTagName('UL')[0];
			if(sub){
				mainMenuItemArray[no].id = 'mainMenuItem' + (no+1);
				var div = document.createElement('DIV');
				div.className='dhtmlgoodies_subMenu';
				document.body.appendChild(div);
				div.appendChild(sub);
				if(slideDirection=='right'){
					div.style.left = getLeftPos(mainMenuItemArray[no]) + mainMenuItemArray[no].offsetWidth + xOffsetSubMenu + 'px';
				}else{
					div.style.left = getLeftPos(mainMenuItemArray[no]) + xOffsetSubMenu + 'px';
				}
				div.style.top = getTopPos(mainMenuItemArray[no]) + 'px';
				div.id = 'subMenuDiv' + (no+1);
				sub.id = 'submenuUl' + (no+1);
				sub.style.position = 'relative';	

				if(navigator.userAgent.indexOf('Opera')>=0){
					submenuObjArray[no+1] = new Array();
					submenuObjArray[no+1]['parentDiv'] = mainMenuItemArray[no];
					submenuObjArray[no+1]['divObj'] = div;
					submenuObjArray[no+1]['ulObj'] = sub;
					submenuObjArray[no+1]['width'] = sub.offsetWidth;
					submenuObjArray[no+1]['left'] = div.style.left.replace(/[^0-9]/g,'');
				}
				sub.style.left = 1 - sub.offsetWidth + 'px';	
				
				// if(document.all)div.style.width = '1px';	
					
				if(navigator.userAgent.indexOf('Opera')<0){
					submenuObjArray[no+1] = new Array();
					submenuObjArray[no+1]['parentDiv'] = mainMenuItemArray[no];
					submenuObjArray[no+1]['divObj'] = div;
					submenuObjArray[no+1]['ulObj'] = sub;
					submenuObjArray[no+1]['width'] = sub.offsetWidth;
					
					
					
					submenuObjArray[no+1]['left'] = div.style.left.replace(/[^0-9]/g,'');
					if(fixedSubMenuWidth)submenuObjArray[no+1]['width'] = fixedSubMenuWidth;
				}	

				if(!document.all)div.style.width = '1px';			
					
			}			
		}
			

		
		
		menuObj.style.visibility = 'visible';
		
		window.onresize = resetPosition;
	}
	
	
	window.onload = initLeftMenu;

