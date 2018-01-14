// 异步获取不同专栏：如“编程”，“读书”和“随笔”等
$('#column-tabs a').click(function(){
    var that = this;
    var $content = $('.tab-content');
    var loading = ['<article><h5>',
                   '<i class="fa fa-spinner fa-spin"></i> ',
                    $(this).text(), '正在加载...',
                    '</h5></article>'].join('');
    var error = ['<article><h5>',
                 '<i class="fa fa-warning"></i> 很抱歉，',
                 $(this).text(), '加载失败...',
                 '</h5></article>'].join('');
    $(this).parent().addClass('active').siblings().removeClass('active');
    history.pushState(null, null, $(this).attr('href'));
    $content.html(loading);
    $.ajax({
        url: that.href,
        method: 'GET',
        dataType: "text",
        success: function(data, textStatus, jqXHR){
            $content.html(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            $content.html(error)
        }
    });
    return false;
})
// 搜索框的客户端验证
$(function(){
    $searchBtn = $('#search-btn');
    $searchBtn.attr('disabled', true)
    $('#search').on('keyup blur', function(){
        reg = /^[\u4e00-\u9fa5a-zA-Z\'\-]+$/;
        if (!this.value){
            $searchBtn.attr('disabled', true);
            $(this).closest('.form-group').removeClass('has-error');
            $('#search-err').text('');
        }else if(reg.test(this.value)){
            $searchBtn.attr('disabled', false);
            $(this).closest('.form-group').removeClass('has-error');
            $('#search-err').text('');
        }else{
            $searchBtn.attr('disabled', true);
            $(this).closest('.form-group').addClass('has-error');
            $('#search-err').text('仅能识别中文或英文关键词')
        }
    })
})
// 标签框中的标签随机分配颜色
colors = ['label-primary', 'label-info', 'label-success', 'label-warning',
          'label-danger']
$(function(){
    $('#tags-box span').each(function(){
        n = Math.floor(Math.random()*5)
        $(this).removeClass('label-danger').addClass(colors[n])
    })
});
