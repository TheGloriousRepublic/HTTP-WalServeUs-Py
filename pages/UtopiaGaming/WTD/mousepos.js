var canvas = null
var mouseX = 0
var mouseY = 0

function getMousePos(canvas, evt) {
	var canvas = document.getElementById('WTD');
	var rect = canvas.getBoundingClientRect();
	return {
		x: evt.clientX - rect.left,
		y: evt.clientY - rect.top
	};
}
var mouseload = function(){
	canvas=document.getElementById('WTD')
	canvas.addEventListener('mousemove', function(evt) {
		var mousePos = getMousePos(canvas, evt);
		mouseX = mousePos.x
		mouseY = mousePos.y
	}, false);
}
