$(document).ready(function(){
	$('#accordion').accordion({collapsible: true, active: false, autoHeight: false});
	$('.refbody').hide();
    $('.refnum').hover(function(event) {
			$(this.nextSibling).toggle();
			event.stopPropagation();
        });
	$('body').click(function(event) {
		$('.refbody').hide();
	});
});