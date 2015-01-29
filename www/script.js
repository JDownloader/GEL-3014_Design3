(function() {

	var canvas = this.__canvas = new fabric.Canvas('myCanvas');
	fabric.Object.prototype.transparentCorners = false;

	var robot = new fabric.Rect({
		width: 50, height: 50, left: 150, top: 100, angle: 45,
		stroke: '#eee', strokeWidth: 10,
		fill: 'rgba(0,0,200,0.5)',
		hasControls: false,
	});

	var rect2 = new fabric.Rect({
		width: 320, height: 220, left: 30, top: 330, angle: 0,
		stroke: '#AEEBAC', strokeWidth: 10,
		fill:'transparent',
		selectable: false,
		hasControls: false,
	});

	function moveRobot(){
		//setRobotPosition(10,10);
		getJSON('http://127.0.0.1:8000/position').then(function(data) {
				setRobotPosition(data.left, data.top);
		});
	}

	function setRobotPosition(left, top) {
		robot.set('left', left);
		robot.set('top', top);
		canvas.calcOffset();
		canvas.renderAll();
	}

	canvas.add(robot, rect2);
	canvas.on({
		'object:moving': onChange,
		'object:scaling': onChange,
		'object:rotating': onChange,
	});

	function onChange(options) {
	}

	document.getElementById("btn1").addEventListener("click", startRun);
	function startRun(){
		$.getJSON('/start').then(function(data) {
			console.log( "Data: " + data );
		}, function(status) { //error detection....
			console.log( "Request Failed: " + status );
		});
	}

	//Refresh part

	var robotStatusHandler = new RobotStatusHandler();
	setInterval(refreshInterface, 250);

	function refreshInterface(){
		$.getJSON('/status').then(function(data) {
			setRobotPosition(data.left, data.top);
			setStatus(data);
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

	//classes

	//Yeah, this is a class
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
		}
		this.refreshValid = function(robotIP) {
			document.getElementById("robotConnectionErrorMessage").innerHTML = "";
			document.getElementById("robotIP").innerHTML = "The IP of your robot is " + data.robotIP;
			document.getElementById("startButton").disabled = false;
		}
		this.refreshInvalid = function(robotIP) {
			document.getElementById("robotConnectionErrorMessage").innerHTML = "Can't contact robot.";
			document.getElementById("robotIP").innerHTML = "";
			document.getElementById("startButton").disabled = true;
		}
	}

})();