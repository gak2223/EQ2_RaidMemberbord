jQuery(function($){
	$(".selectable").jQselectable({
		show: "fadeIn",
		showDuration: "fast",
		opacity: .9
	});
	
	$('#add').click(function() { 
		$('#refresh').append('<option value="value_' + num + '">value_' + (num++) + '</option>');
		jQs2.refresh();
	});
	
	// change skins but not for IE
	if(document.all){
		$("#skin").remove();
	}else{
		var css = $("link[type='text/css']");
		$("#skin a").click(function(){
			var href = this.href.split("#")[1];
			css[1].href = css[1].href.replace(/(skin\/)\w+(\/style.css)/,"$1"+href+"$2");
			return false;
		});
	}
});

