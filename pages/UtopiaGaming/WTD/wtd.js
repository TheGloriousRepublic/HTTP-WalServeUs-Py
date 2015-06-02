var canvas = null
var ctx = null
var towers = []
var validTowers = ["walrus", "cat", "cheatbot"]
var track = "default"
var paused = false

Array.prototype.contains = function(obj) { //Function to detect if an array contains an object
	var i = this.length;
	while (i--) {
		if (this[i] === obj) {
			return true;
		}
	}
	return false;
}

function tower(name, x, y, rot){ //The tower class
	this.name = name; //Tower ID
	this.x = x; //Tower position x
	this.y = y; //Tower position y
	this.img = new Image(); 
	this.img.src = "images/towers/"+name+".png"; //Tower image
	this.imgwidth = 75;  //Tower dimensions
	this.imgheight = 75; //^^^^^ ^^^^^^^^^^
	this.img.title = name //Hovertext (will this even work?)
	
	this.img.addEventListener('click', function(){alert("Hello, world!");}, false);
	this.draw = function(){ //To create the tower
		ctx.drawImage(this.img, this.x, this.y, this.imgwidth, this.imgheight);
	}
};

var pause = function(){
	paused = true;
}

var unpause = function(){
	paused = false;
}

var togglePause = function(){
	if(paused) {
		paused = false
	} else {
		paused = true
	}
}

var onTrack = function(trackname, x, y){
	return false //will implement later later
};


var addTower = function(name, x, y){
	if(validTowers.contains(name)){
		if(!(onTrack(track, x, y))) {
			towers.push(new tower(name, x, y, 0));
		}
		
	} else {
		addTower("cheatbot", x, y); //Easter Egg
	}
	update();
};

var removeTower = function(index){
	towers.splice(index, index);
	update();
};

var drawTowers = function(){
	for(var t = 0; t<towers.length; t++){
		towers[t].draw();
	}
	return(true);
};

var drawPalleteIcons = function() {
	
};

var buildBasePallete = function() {
	ctx.fillStyle = "#D1DBDD"; //Tower Pallette Coloration
	ctx.fillRect(600, 0, 800, 600); //Tower Palette
	ctx.fillStyle = "#A1ABAD"; //Bolt Coloration
	for(i=30; i<870; i+=30) { //Render bolts
		ctx.arc(610,i,2,0,Math.PI*2,false);
	}
	ctx.fill();
	console.log("Pallete Built"); //for debugging
	drawPalleteIcons();
	
};

var wtd = function() {
	canvas = document.getElementById('WTD'); //register variables
	ctx = canvas.getContext('2d'); //Canvas context
	canvas.addEventListener('click', function(){update();}, false);
	buildBasePallete(); //Build the tower pallete
	
	ctx.save();
	
};

var update = function() {
	ctx.restore();
	ctx.save();
	
	drawPalleteIcons();
	drawTowers();
	console.log("Canvas updated")
};

var test = function() {
	addTower("walrus", 50, 50);
	addTower("cat", 100, 100);
	addTower("cheatbot", 50, 100);
	return(true);
};