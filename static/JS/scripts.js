function toggleFullScreen() {
            // Implement the full-screen mode code here
            var element = document.documentElement;
            if (!document.fullscreenElement) {
                element.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        }

        function changeFontSize(changeAmount) {
            // Implement the font size change code here using 'changeAmount'
            var currentSize = parseInt($('#extractedText').css('font-size'));
            var newSize = currentSize + changeAmount;
            $('#extractedText').css('font-size', newSize + 'px');
        }

        $(document).ready(function() {
    // فور تحميل الصفحة، قم بتشغيل الوضع الليلي
    $('body').addClass('night-mode');
  });

  // دالة لتبديل الوضع
  function toggleNightMode() {
    $('body').toggleClass('night-mode');
  }

        function changeFontFamily(selectedFont) {
            // Implement the font family change code here using 'selectedFont'
            $('#extractedText').css('font-family', selectedFont);
        }

        $('#fontSelect').change(function () {
            var selectedFont = $(this).val();
            changeFontFamily(selectedFont);
        });

        $('.control-button').click(function () {
            // Handle common button click actions here, if needed
        });
        
// تكبير حجم الخط باستخدام span
$('#increaseFontSize').click(function () {
    changeFontSize(2); // يمكنك ضبط القيمة حسب احتياجاتك
});

// تصغير حجم الخط باستخدام span
$('#decreaseFontSize').click(function () {
    changeFontSize(-2); // يمكنك ضبط القيمة حسب احتياجاتك
});

