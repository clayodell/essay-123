$(document).ready(function(){
	count = 0;
	countLimit = 3;
	$('#add-tag').click(function(e){
		e.preventDefault();
		var tagValue = $.trim($('.tags-value').val());
		if(tagValue == '') {
			$('.tags-controlgroup').addClass('error');
			$('.tags-error').html('Keyword cannot be blank');
			$('.tags-error').css('display','block');
		}
		else if(tagExists(tagValue)) {
			$('.tags-controlgroup').addClass('error');
			$('.tags-error').html('You have already added this keyword');
			$('.tags-error').css('display','block');
		}
		else {
			count = getExistingTagsCount()
			if(count<countLimit) {
				checkErrorBefore();
				var tagValue = $('.tags-value').val();
				var tagsHTML = "<span class='"+tagValue+" tag'><input type='hidden' name='tags[]' value="+tagValue+" class='"+tagValue+"'/> <span class='label label-info'><a href='"+tagValue+"' class='remove-tag'><i class='icon-remove icon-white'></i></a><span class='tag-value'>"+tagValue+"</span></span></span>";
				$('.tags-container').append(tagsHTML);
				$('.tags-value').val('');
			}
			else {
				$('.tags-controlgroup').addClass('error');
				$('.tags-error').html('You can add maximum of '+countLimit +" keywords");
				$('.tags-error').css('display','block');
				$('.tags-value').val('');
			}
			
		}
	});
	
	$(document).on('click', 'a.remove-tag', function(e) {
			e.preventDefault();
			var toRemove = ($(this).attr('href'));
			$("."+toRemove).remove();
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

function getExistingTagsCount(){
	return $('.tags-container').children('.tag').size()
}

function tagExists(tagValue) {
	if($('.'+tagValue).length != 0) {
		return true;
	}
	else {
		return false;
	}
}