// 将客户端验证抽象为函数，应用于文章页“评论表单”和所有动态加载的“回复表单”
function checkAndPost(){
    var $form = $(this); //该函数将会被绑定到表单对象
    var nickname, email, content;
    var $submit = $('button[type="submit"]', $form).attr('disabled', true);

    $(':input', $form).on('keyup blur', function(){
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
        function inputError(){
            $input.closest('.form-group').addClass('has-error')
                   .end().parent().next('h5')
                   .html(['<i class="fa fa-close text-danger"></i>',
                          '&nbsp;系统无法识别,请重新检查'].join(''));
            $submit.attr('disabled', true);
        };
        // 验证nickname,email和content字段
        if($(this).is('[name="nickname"]')){
            var nameVal = $.trim(this.value);
            var regName = /^[\u4e00-\u9fa50-9a-zA-Z.@_-]+$/;
            if(nameVal=='' || !regName.test(nameVal)){
                nickname = '';
                inputError();
            }else{
                nickname = nameVal;
                inputSuccess();
            }
        };
        if($(this).is('[name="email"]')){
            var emailVal = $.trim(this.value)
            var regEmail = /^(\w)+(\.\w+)*@(\w+)((\.\w+)+)$/;
            if(emailVal=='' || !regEmail.test(emailVal)){
                email = '';
                inputError();
            }else{
                email = emailVal;
                inputSuccess();
            }
        };
        if($(this).is('[name="content"]')){
            var contentVal = $.trim(this.value);
            if(contentVal==''||contentVal.length > 1000){
                content = '';
                inputError();
                if(contentVal.length>1000){
                    $(this).parent().next('h5').html([
                        '<i class="fa fa-exclamation text-danger"></i>&nbsp;',
                        '最多输入1000字，已超出&nbsp;<strong class="text-danger">',
                         contentVal.length-1000, '</strong>&nbsp;字'
                     ].join(''))
                };
            }else{
                content = contentVal;
                inputSuccess();
            }
        }
    });
    // 点击提交按钮，异步提交表单
    $submit.click(function(){
        var csrftoken = $('[name="csrfmiddlewaretoken"]', $form).val();
        $submit.button('loading');
        $.ajax({
            url: $form.attr('action'),
            method: 'POST',
            dataType: 'text',
            data: {
                nickname: nickname,
                email: email,
                content: content,
                csrfmiddlewaretoken: csrftoken // 同时发送 csrf_token
            },
            success: function(data, textStatus, jqXHR){
                $form[0].reset();
                $('.form-group > h5', $form).empty();
                nickname = email = content = '';
                $submit.removeClass('disabled')
                       .attr('disabled', true)
                       .text('提交');
                // 针对“评论表单”和“回复表单”做不同处理
                if ($form.parent('#comment-add')[0] != undefined){ // 评论表单
                    $('#comment-list > h4:first').after(data);
                    var top = $('#comment-list').offset().top - 100;
                    $('html, body').scrollTop(top);
                }else{ // "回复表单"
                    $form.hide();
                    $form.prev('p').find('.subcomment-add').text('回复');
                    $form.parent('.comment').after(data);
                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                alert('Error:' + errorThrown);
                $submit.removeClass('disabled')
                       .attr('disabled', true)
                       .text('提交');
            }
        });
        return false;
    })
};
// 对评论表单绑定checkAndPost函数
$(function(){
    $('form').each(checkAndPost);
})
// 点击回复按钮，动态加载、收起、显示“回复表单”，绑定checkAndPost函数
$('#comment-list').on('click', '.subcomment-add', function(){
    var that = this;
    var $existForm = $(this).closest('.comment').children('form');
    //如果表单不存在就创建并添加一个新表单,将文字改为"收起"
    if ($existForm[0] == undefined){
        var $newForm = $('#comment-add form').clone();
        $newForm.attr('action', $(this).attr('data-target'));
        $(':input[id^="comment"]', $newForm).each(function(){
            //修改id 如id="comment-nickname"改为"sub-of-comment-1-nickname"
            this.id = this.id.replace('comment', that.id);
            $(this).val('')
                   .parent().next('h5').empty()
                   .closest('.form-group').removeClass('has-error');
        });
        $('label[for^="comment"]', $newForm).each(function(){
            //修改字段标签的for属性 如for="comment-nickname"改为"sub-of-comment-1-nickname"
            forVal = $(this).attr('for').replace('comment', that.id);
            $(this).attr('for', forVal);
        });
        // 绑定checkAndPost函数
        $newForm.appendTo($(this).closest('.comment'))
                .each(checkAndPost);
        // 添加“关闭”按钮
        var closeBtn = ['<button type="button" class="btn ',
                        'btn-danger btn-close">关闭</button>'].join('');
        // 加载表单
        $('[type="submit"]', $newForm).parent().append($(closeBtn));
        $newForm[0].reset();
        $(this).text('收起').addClass('text-danger');
    //如果表单存在且可见,收起表单,将文字改为"回复"
    }else if($existForm.is(':visible')){
        $existForm.hide();
        $(this).text('回复').removeClass('text-danger');
    //如果表单存在且不可见,显示表单,将文字改为"收起"
    }else{
        $existForm.show();
        $(this).text('收起').addClass('text-danger');
    }
})
// 点击“回复表单”的“关闭”按钮，收起表单
$('#comment-list').on('click', '.btn-close', function(){
    $(this).closest('.comment')
           .find('.subcomment-add').removeClass('text-danger').text('回复');
    $(this).closest('form').hide();
})
// 对评论点赞
$(function(){
    $('#comment-list').on('click', '.comment-up', function(){
        var $icon = $('.fa', $(this));
        var addNum = $icon.hasClass('fa-thumbs-o-up') ? '1' : '-1';
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url: $(this).attr('data-target'),
            method: 'POST',
            dataType: 'text',
            data: {
                addNum: addNum,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(data, textStatus, jqXHR){
                if (addNum == '1'){
                    $icon.removeClass('fa-thumbs-o-up')
                         .addClass('fa-thumbs-up')
                         .html('&nbsp;('+ data +')')
                }else{
                    $icon.removeClass('fa-thumbs-up')
                         .addClass('fa-thumbs-o-up')
                         .html('&nbsp;('+ data +')')
                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                alert('Error:' + errorThrown);
            }
        });
    })
})
// 异步获取更多评论
$('#main-content').on('click', '#comment-more > a', function(){
    var that = this;
    $(this).html('<i class="fa fa-spinner fa-spin"></i> 正在加载');
    $.ajax({
        url: this.href,
        method: 'GET',
        dataType: "text",
        success: function(data, textStatus, jqXHR){
            $(that).parent().replaceWith(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            $(that).html('<i class="fa fa-warning"></i> 加载失败: ' + errorThrown)
        }
    });
    return false;
})
