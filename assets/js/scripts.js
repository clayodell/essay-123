$(document).ready(function(){
	count = 0;
	countLimit = 3;
	$('#add-tag').click(function(e){
		e.preventDefault();
		if($('.tags-value').val() == '') {
			$('.tags-controlgroup').addClass('error');
			$('.tags-error').html('Keyword cannot be blank');
			$('.tags-error').css('display','block');
		}
		else {
			if(count<countLimit) {
				checkErrorBefore();
				var tagValue = $('.tags-value').val();
				var tagsHTML = "<span class='"+tagValue+"'><input type='hidden' name='tags[]' value="+tagValue+" class='"+tagValue+"'/> <span class='label label-info'><a href='"+tagValue+"' class='remove-tag'><i class='icon-remove icon-white'></i></a><span class='tag-value'>"+tagValue+"</span></span></span>";
				$('.tags-container').append(tagsHTML);
				count += 1;
				$('.tags-value').val('');
			}
			else {
				$('.tags-controlgroup').addClass('error');
				$('.tags-error').html('You can add masimum of '+countLimit + "keywords");
				$('.tags-error').css('display','block');
				$('.tags-value').val('');
			}
		}
	});
	
	$(document).on('click', 'a.remove-tag', function(e) {
			e.preventDefault();
			var toRemove = ($(this).attr('href'));
			$("."+toRemove).remove();
			count -= 1;
	});
	
});

function checkErrorBefore(){
	if($('.tags-controlgroup').hasClass('error')){
		$('.tags-controlgroup').removeClass('error');
		$('.tags-error').css('display','none');
		$('.tags-error').html('');
	}
}

function validateTopicForm(){
	resetFormValidation();
	var flag;
	if($('#inputTitle').val() == ''){
		$('.title-controlgroup').addClass('error');
		$('.title-error').html('Title cannot be left blank');
		$('.title-error').css('display','block');
		flag = false;
	}
	if($('#inputDescription').val() == "") {
		$(".description-controlgroup").addClass('error');
		$('.description-error').html('Description cannot be left blank');
		$('.description-error').css('display','block');
		flag = false;
	}
	
	return flag;
}
function resetFormValidation(){
	$('.help-inline').css('display','none');
	$('.help-inline').html('');
	$('.control-group').removeClass('error');
}