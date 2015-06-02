$(document).ready(function(){
	$('#accordion').accordion({collapsible: true, active: false, autoHeight: false});
	$('.refbody').hide();
    $('.refnum').click(function(event) {
			$(this.nextSibling).toggle();
			event.stopPropagation();
        });
	$('body').click(function(event) {
		$('.refbody').hide();
	});
});