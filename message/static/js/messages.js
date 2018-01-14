// 异步加载留言
$(function(){
	$('#msg-menu').on('click', 'button', function(){
		var that = this;
		var $link = $('a', $(this));
		var $list = $('#msg-list');
		$.ajax({
			url: $link.attr('href'),
			method: 'GET',
			dataType: "text",
			success: function(data, textStatus, jqXHR){
				$(that).addClass('btn-info').siblings().removeClass('btn-info');
				$list.html($(data));
				history.pushState(null, null, $link.attr('href'));
			},
			error: function(jqXHR, textStatus, errorThrown){
				alert('加载失败。原因: ' + errorThrown)
			}
		});
		return false;
	})
})
// 异步加载更多
$('#main-content').on('click', '#msg-more > a', function(){
    var that = this;
    $(this).html('<i class="fa fa-spinner fa-spin"></i> 正在加载');
    $.ajax({
        url: this.href,
        method: 'GET',
        dataType: "text",
        success: function(data, textStatus, jqXHR){
            $(that).parent().replaceWith($(data))
        },
        error: function(jqXHR, textStatus, errorThrown){
            $(that).html('<i class="fa fa-warning"></i> 加载失败: ' + errorThrown)
        }
    });
    return false;
})
// 对必填项加上星号(*)
$('#msg-form :input[required="required"]').each(function(){
    $(this).parent().prev().append('<i class="text-danger"> *</i>')
})
// 留言表单的客户端验证以及异步提交
$(function(){
    var nickname, email, content;
    var $submit = $('button[type="submit"]').attr('disabled', true);

    $('#msg-form :input').on('keyup blur', function(){
		var $input = $(this);
		// 表单字段验证通过时
		function inputSuccess(){
			$input.closest('.form-group').removeClass('has-error')
				   .end().parent().next('h5')
				   .html('<i class="fa fa-check text-success"></i>');
			if(nickname && email && content){
				$submit.attr('disabled', false);
			};
		};
		// 表单字段验证未通过时
		function inputError(info){
			$input.closest('.form-group').addClass('has-error')
				   .end().parent().next('h5')
				   .html('<i class="fa fa-close fa-exclamation"></i>&nbsp;' + info);
			$submit.attr('disabled', true);
		};
		// 验证nickname,email和content字段
        if($(this).is('#nickname')){
            var nameVal = $.trim(this.value);
            var regName = /^[\u4e00-\u9fa50-9a-zA-Z.@_-]+$/;
            if(nameVal=='' || !regName.test(nameVal)){
				nickname = '';
                inputError('空值或含特殊字符');
            }else{
				nickname = nameVal;
				inputSuccess();
            }
        };
        if($(this).is('#email')){
            var emailVal = $.trim(this.value)
            var regEmail = /^(\w)+(\.\w+)*@(\w+)((\.\w+)+)$/;
            if(emailVal=='' || !regEmail.test(emailVal)){
				email = '';
                inputError('不完整或格式错误');
            }else{
				email = emailVal;
                inputSuccess();
            }
        };
        if($(this).is('#content')){
            var contentVal = $.trim(this.value);
            if(contentVal==''||contentVal.length > 500){
				content = '';
                if(contentVal == ''){
                    inputError('已输入&nbsp;0&nbsp;字');
                }else{
                    inputError(['已超出&nbsp;', contentVal.length-500,
							    '&nbsp;字</h5><h5>(最多输入500字)'].join(''))
                }
            }else{
				content = contentVal;
                inputSuccess(['<span class="text-info">已输入&nbsp;',
                              contentVal.length, '&nbsp;字</span>'].join(''));
            }
        }
    });
	// 异步提交表单
    $submit.click(function(){
        var gender = $('input[name="gender"]:checked').val();
        var types = $('input[name="types"]:checked').val();
        var notice = $('#notice')[0].checked ? true : false;
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        $submit.button('loading');
        $.ajax({
            url: '/message/create/',
            method: 'POST',
            dataType: 'text',
            data: {
                nickname: nickname,
                gender: gender,
                email: email,
                types: types,
                content: content,
                notice: notice,
                csrfmiddlewaretoken: csrftoken // 同时传送 csrf_tokon
            },
            success: function(data, textStatus, jqXHR){
				// 处理服务器端表单通过验证(form_valid)时返回的数据
                if (data.indexOf('form-invalid') == -1){
                    $('.modal-backdrop').detach();
					$('#msg-form')[0].reset();
					nickname = email = content = '';
	                $submit.removeClass('disabled')
					       .attr('disabled', true)
						   .text('提交');
					$('.form-group > h5').empty();
                    $('#msg-modal').fadeOut('slow', function(){
                        alert(data);
                    });
				// 处理服务器端表单未能通过验证(form_invalid)时返回的数据
                }else{
                    $data = $(data);
                    $nameErr = $('#nickname-errors', $data).html();
                    if ($nameErr){
                        $('#nickname').closest('.form-group').addClass('has-error')
							   		  .end().parent().next('h5').html($nameErr);
                    };
                    $emailErr = $('#email-errors', $data).html();
                    if ($emailErr){
                        $('#email').closest('.form-group').addClass('has-error')
							   	   .end().parent().next('h5').html($emailErr);
                    };
                    $contentErr = $('#content-errors', $data).html();
                    if ($contentErr){
                        $('#content').closest('.form-group').addClass('has-error')
							   		 .end().parent().next('h5').html($contentErr);
                    }
                    $nonFieldErr = $('#non-field-errors', $data).html();
                    if ($nonFieldErr){
                        $('.modal-header').append($nonFieldErr);
                    };
	                $submit.button('reset');
                };

            },
            error: function(jqXHR, textStatus, errorThrown){
                alert('Error:' + errorThrown);
				$submit.button('reset');
            }
        });
        return false;
    })
})
