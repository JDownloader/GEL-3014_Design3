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
	colors['black_p'] = 'rgba(0,0,0,0.5)';
	colors['blue_p'] = 'rgba(0,0,255,0.5)';
	colors['red_p'] = 'rgba(255,0,0,0.5)';
	colors['yellow_p'] = 'rgba(255,255,0,0.5)';
	colors['white_p'] = 'rgba(255,255,255,0.5)';
	colors['green_p'] = 'rgba(0,255,0,0.5)';

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

	function setRobotPosition(data) {
        var x = robot.setPosition(data.left, data.top, data.angle);
        var y = robot.drawPath(data.path, data.top, data.angle);
        var z = robot.drawOldPositions(data.last_known_positions);
		planCanvas.calcOffset();
		planCanvas.renderAll();
	}

	var robot = new RobotForm();
    robot.addToCanvas(planCanvas);
	planCanvas.add(greenLines);

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

	document.getElementById("startButton").addEventListener("click", startRun);
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

	var robotContextHandler = new RobotContextHandler();
	setInterval(refreshInterface, 250);

	function refreshInterface(){
		$.getJSON('/context').then(function(data) {
			setRobotPosition(data);
			setContext(data);
			setFlag(data.flag);
			setCubes(data.cubes);
			document.getElementById("baseConnectionErrorMessage").innerHTML = "";
			if(data.kinect_is_fake){
				document.getElementById("baseConnectionErrorMessage").innerHTML = "The kinect is mocked.";
			}
		}, function(status) { //error detection....
			console.log( "Request Failed: " + status );
			document.getElementById("baseConnectionErrorMessage").innerHTML = "Can't contact base server.";
		});
	}

	function setContext(data){
		document.getElementById("chrono").innerHTML = data.chrono;
		document.getElementById("question").innerHTML = data.question;
		document.getElementById("answer").innerHTML = data.answer;
		robotContextHandler.updateContext(data);
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
				flagCubes[i].strokeWidth = 0;
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
                planCubes[i].strokeWidth = 1;
			} else{
				planCubes[i].fill = 'rgba(0,0,0,0)';
                planCubes[i].strokeWidth = 0;
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

	function RobotForm () {
        this.robotBody = new fabric.Rect({
            width: 50, height: 50, left: 150, top: 100, angle: 45,
            stroke: '#eee',
            strokeWidth: 10,
            fill: 'rgba(0,0,200,0.5)',
            hasControls: false,
            originX: 'center',
            originY: 'center'
        });
        this.purpleCorner = new fabric.Rect({
            width: 20, height: 20, left: 150, top: 100, angle: 45,
            fill: 'rgba(128,0,128,1)',
            hasControls: false,
        });
        this.greenCorner = new fabric.Rect({
            width: 20, height: 20, left: 150, top: 100, angle: 45,
            fill: 'rgba(0,128,0,1)',
            hasControls: false,
            originY: 'bottom',
            originX: 'right'
        });
        this.orange1Corner = new fabric.Rect({
            width: 20, height: 20, left: 150, top: 100, angle: 45,
            fill: 'rgba(255,140,0,1)',
            hasControls: false,
            originY: 'bottom',
            originX: 'left'
        });
        this.orange2Corner = new fabric.Rect({
            width: 20, height: 20, left: 150, top: 100, angle: 45,
            fill: 'rgba(255,140,0,1)',
            hasControls: false,
            originY: 'top',
            originX: 'right'
        });
        this.lines = new Array();
        for(i=0; i<3; i++){
            this.lines[i] = new fabric.Line([0,0,100,100], {
                fill: 'red',
                stroke: 'red',
                strokeWidth: 5,
                selectable: false
            });
        }
        this.lastKnowPositions = new Array();
        for (i = 0; i < 10; i++){
            var cube = new fabric.Rect({
                width: 15, height: 15, left: 150, top: 100, angle: 0,
                fill: 'rgba(0,0,0,0.5)',
                hasControls: false,
            });
            this.lastKnowPositions[i] = cube;
        }

        this.addToCanvas = function(canvas){
            canvas.add(this.robotBody, this.purpleCorner, this.greenCorner, this.orange1Corner, this.orange2Corner);
            for(i=0; i<this.lines.length; i++){
                canvas.add(this.lines[i]);
            }
            for(i=0; i<this.lastKnowPositions.length; i++){
                canvas.add(this.lastKnowPositions[i]);
            }
        };

        this.setPosition = function(x, y, angle){
            var x_pos = x;
            var y_pos = y;
            //console.log(x_pos);
            this.robotBody.set('left', x_pos);
            this.robotBody.set('top', y_pos);
            this.robotBody.set('angle', angle);
            this.purpleCorner.set('left', x_pos);
            this.purpleCorner.set('top', y_pos);
            this.purpleCorner.set('angle', angle);
            this.greenCorner.set('left', x_pos);
            this.greenCorner.set('top', y_pos);
            this.greenCorner.set('angle', angle);
            this.orange1Corner.set('left', x_pos);
            this.orange1Corner.set('top', y_pos);
            this.orange1Corner.set('angle', angle);
            this.orange2Corner.set('left', x_pos);
            this.orange2Corner.set('top', y_pos);
            this.orange2Corner.set('angle', angle);
            return null;
        };
        this.drawPath = function(path, x, y){
            //this.
			for(i = 0; i < this.lines.length; i++) {
                if(i < path.length-1){
                    this.lines[i].set('x1', path[i][0]);
                    this.lines[i].set('y1', path[i][1]);
                    this.lines[i].set('x2', path[i+1][0]);
                    this.lines[i].set('y2', path[i+1][1]);
                    this.lines[i].setCoords();
                }else{
                    this.lines[i].set('x1', 0);
                    this.lines[i].set('y1', 0);
                    this.lines[i].set('x2', 0);
                    this.lines[i].set('y2', 0);
                    this.lines[i].setCoords();
                }
            }
            return null;
        }
        this.drawOldPositions = function(positions){
			for(i = 0; i < this.lastKnowPositions.length; i++) {
                if(i < positions.length){
                    this.lastKnowPositions[i].set('left', positions[i][0]);
                    this.lastKnowPositions[i].set('top', positions[i][1]);
                    this.lastKnowPositions[i].fill = 'rgba(0,204,215,0.5)';
                }else{
                    this.lastKnowPositions[i].fill = 'rgba(0,0,0,0)';
                }
            }
            return null;
        }
    }

	function RobotContextHandler () {
		this.valid = null;
		this.updateContext = function(data) {
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
