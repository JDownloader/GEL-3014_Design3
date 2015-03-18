(function() {

	var planCanvas = new fabric.Canvas('planCanvas');
	var flagCanvas = new fabric.Canvas('flagCanvas');
	var currentFlag;
	var currentCubes;
	var colors = {};
	colors['black'] = 'rgba(0,0,0,1)';
	colors['blue'] = 'rgba(0,0,255,1)';
	colors['red'] = 'rgba(255,0,0,1)';
	colors['yellow'] = 'rgba(255,255,0,1)';
	colors['white'] = 'rgba(255,255,255,1)';
	colors['green'] = 'rgba(0,255,0,1)';
	colors['black_p'] = 'rgba(0,0,0,0.2)';
	colors['blue_p'] = 'rgba(0,0,255,0.2)';
	colors['red_p'] = 'rgba(255,0,0,0.2)';
	colors['yellow_p'] = 'rgba(255,255,0,0.2)';
	colors['white_p'] = 'rgba(255,255,255,0.2)';
	colors['green_p'] = 'rgba(0,255,0,0.2)';

	fabric.Object.prototype.transparentCorners = false;

	function compareTbl(tblA, tblB){
		var areTheSame = true;
		if(tblA == null || tblB == null){
			areTheSame = false;
		} else{
			var lenA = tblA.length;
			var lenB = tblB.length;
			if(lenA === lenB){
				for(i = 0; i < lenA; i++) {
					if(tblA[i] != tblB[i]) {
						areTheSame = false;
						break;
					}
				}
			} else{
				areTheSame = false
			}
		}
		return areTheSame;
	}

	//planCanvas

	var robot = new fabric.Rect({
		width: 50, height: 50, left: 150, top: 100, angle: 45,
		stroke: '#eee',
		strokeWidth: 10,
		fill: 'rgba(0,0,200,0.5)',
		hasControls: false,
	});

	var planCubes = new Array();
	for (i = 0; i < 10; i++){
		var cube = new fabric.Rect({
			width: 22, height: 22, left: 150, top: 100, angle: 0,
			fill: 'rgba(0,0,0,0)',
			stroke: '#000',
			strokeWidth: 1,
			hasControls: false,
		});
		planCanvas.add(cube);
		planCubes[i] = cube;
	}


	var greenLines = new fabric.Rect({
		width: 178, height: 178, left: 61, top: 363, angle: 0,
		stroke: '#AEEBAC', strokeWidth: 10,
		fill:'transparent',
		selectable: false,
		hasControls: false,
	});

	function setRobotPosition(left, top) {
		robot.set('left', left);
		robot.set('top', top);
		planCanvas.calcOffset();
		planCanvas.renderAll();
	}

	planCanvas.add(robot, greenLines);
	planCanvas.on({
		'object:moving': onChange,
		'object:scaling': onChange,
		'object:rotating': onChange,
	});

	function onChange(options) {
	}

	//flagCanvas

	var flagCubes = new Array();
	for (y = 0; y < 3; y++){
		for (x = 0; x < 3; x++){
			var cube = new fabric.Rect({
				width: 50, height: 50, left: y*60+10, top: x*60+10, angle: 0,
				fill: 'rgba(0,0,200,0.1)',
				hasControls: false,
			});
			flagCanvas.add(cube);
			flagCubes[x + y*3] = cube;
		}
	}
	greenLines.moveTo(0);

	//Events

	document.getElementById("btn1").addEventListener("click", startRun);
	function startRun(){
		$.getJSON('/start').then(function(data) {
			console.log( "Data: " + data );
		}, function(status) { //error detection....
			console.log( "Request Failed: " + status );
		});
	}

	$(".dropdown-menu li a").click(function(){
		var selText = $(this).text();
		$(this).parents('.btn-group').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
	});

	$("#ddTable").click(function(){
		alert($('.ddTable').text());
	});

	//Refresh part

	var robotStatusHandler = new RobotStatusHandler();
	setInterval(refreshInterface, 250);

	function refreshInterface(){
		$.getJSON('/status').then(function(data) {
			setRobotPosition(data.left, data.top);
			setStatus(data);
			setFlag(data.flag);
			setCubes(data.cubes);
			document.getElementById("baseConnectionErrorMessage").innerHTML = "";
		}, function(status) { //error detection....
			console.log( "Request Failed: " + status );
			document.getElementById("baseConnectionErrorMessage").innerHTML = "Can't contact base server.";
		});
	}

	function setStatus(data){
		document.getElementById("chrono").innerHTML = data.chrono;
		robotStatusHandler.updateStatus(data);
	}

	function setFlag(baseFlag){
		if(!compareTbl(currentFlag, baseFlag)){
			currentFlag = baseFlag;
			refreshFlag(baseFlag);
		}
	}

	function refreshFlag(baseFlag){
		for (i = 0; i < 9; i++){
			if(baseFlag[i] === null) {
				flagCubes[i].fill = 'rgba(0,0,0,0)';
			} else{
				flagCubes[i].fill = colors[baseFlag[i]];
				flagCubes[i].stroke = '#000';
				flagCubes[i].strokeWidth = 2;
			}
		}
		flagCanvas.calcOffset();
		flagCanvas.renderAll();
	}

	function setCubes(cubes){
		if(true){
			currentCubes = cubes;
			refreshCubes(cubes);
		}
	}

	function refreshCubes(cubes){
		for(i = 0, len = cubes.length; i < 10; i++){
			if(i < len){
				setCubePlanCanvasPosition(cubes[i][0], cubes[i][1], planCubes[i])
				planCubes[i].fill = colors[cubes[i][2]];
			} else{
				planCubes[i].fill = 'rgba(0,0,0,0)';
			}
		}
		planCanvas.calcOffset();
		planCanvas.renderAll();
	}

	function setCubePlanCanvasPosition(x, y, cube){
		canvasWidth = planCanvas.width;
		canvasHeight = planCanvas.height;
		cubeLeft = canvasWidth - 11 - x / 1120 * canvasWidth;
		cubeTop = canvasHeight - 11 - y / 2230 * canvasHeight;
		cube.set('left', cubeLeft);
		cube.set('top', cubeTop);
	}

	//Classes

	function RobotStatusHandler () {
		this.valid = null;
		this.updateStatus = function(data) {
			newValid = false;
			if(data.robotIP === "0.0.0.0"){
				newValid = false;
			} else{
				newValid = true;
			}
			if(this.valid != newValid){
				this.valid = newValid;
				this.refresh(data.robotIP)
			}
		};
		this.refresh = function(robotIP){
			if(this.valid) {
				this.refreshValid(robotIP);
			} else{
				this.refreshInvalid(robotIP);
			}
		};
		this.refreshValid = function(robotIP) {
			document.getElementById("robotConnectionErrorMessage").innerHTML = "";
			document.getElementById("robotIP").innerHTML = "The IP of your robot is " + robotIP;
			document.getElementById("startButton").disabled = false;
		};
		this.refreshInvalid = function(robotIP) {
			document.getElementById("robotConnectionErrorMessage").innerHTML = "Can't contact robot.";
			document.getElementById("robotIP").innerHTML = "";
			document.getElementById("startButton").disabled = true;
		}
	}

})();