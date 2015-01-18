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

	document.getElementById("btn1").addEventListener("click", moveRobot);

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

	//Refresh part

	setInterval(refreshInterface, 250);

	function refreshInterface(){
		$.getJSON('http://127.0.0.1:8000/position').then(function(data) {
			setRobotPosition(data.left, data.top);
			document.getElementById("baseConnectionErrorMessage").innerHTML = "";
		}, function(status) { //error detection....
			console.log( "Request Failed: " + status );
			document.getElementById("baseConnectionErrorMessage").innerHTML = "Can't contact base server.";
		});
	}

})();