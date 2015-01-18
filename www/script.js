(function() {
		var getJSON = function(url) {
			return new Promise(function(resolve, reject) {
				var xhr = new XMLHttpRequest();
				xhr.open('get', url, true);
				xhr.responseType = 'json';
				xhr.onload = function() {
					var status = xhr.status;
					if (status == 200) {
						resolve(xhr.response);
					} else {
						reject(status);
					}
				};
				xhr.send();
			});
		};

		getJSON('http://127.0.0.1:8000/position').then(function(data) {
				setRobotPosition(data.left, data.top);
		}, function(status) { //error detection....
			alert('Something went wrong.');
		});
		
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
		setRobotPosition(10,10);
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
})();