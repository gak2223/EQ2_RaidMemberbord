/*MainのScript*/
jQuery(function($){
	$("#datepicker").datepicker(
	{
		showAnim: 'drop',
		minDate: '-10d',
		maxDate: '+15d',
		dateFormat: 'yy-mm-dd'
	});
});
