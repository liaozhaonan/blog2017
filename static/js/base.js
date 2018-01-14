// 导航栏：当前页高亮
$(function(){
    var urlstr = location.origin + location.pathname;
    $('.navbar-nav a').each(
        function(){
            if (this.href == urlstr){
                $(this).parent().addClass('active')
                    .siblings().removeClass('active');
            }
        }
    )
})
// 回到顶部按钮
$(function(){
    $backToTop = $('#back-to-top');
    $(window).scroll(function(){
        if($(window).scrollTop() > 200){
            $backToTop.fadeIn(1500);
        }else{
            $backToTop.fadeOut(1500);
        }
    });
    $backToTop.click(function(){
        $('body, html').animate({
            scrollTop: 0
        }, 500);
        return false;
    })
})
// 异步获取上下页
$('#main-content').on('click', '.pager li:not(.disabled) > a', function(){
    var $content = $('#articles-of-page');
    history.pushState(null, null, $(this).attr('href'));
    $.ajax({
        url: this.href,
        method: 'GET',
        dataType: "text",
        success: function(data, textStatus, jqXHR){
            $content.html(data);
            $('body, html').animate({
                scrollTop: 0
            });
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert('Error: ' + errorThrown)
        }
    });
    return false;
})
