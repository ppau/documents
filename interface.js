	window.requestAnimationFrame = window.requestAnimationFrame || 
        function(x) { setTimeout(x, 1000) };

    if (window.addEventListener) {
      var hashchange = function() {
          if (location.hash.substr(1) === "") { return; }

          var page = document.querySelector('.page'),
              node = document.getElementById(location.hash.substr(1)),
              hl = document.querySelector('.hl');

          if (node == null) return;
          
          if (hl != null) {
            hl.parentNode.removeChild(hl);
          }
          
          hl = document.createElement('div');
          hl.className = 'hl';

          hl.style.top = node.offsetTop - 8;
          hl.style.left = 0;

          if (node.nodeName == "DT") {
            hl.style.height = node.offsetHeight + 32 + node.nextElementSibling.offsetHeight;
          } else {
            hl.style.height = node.offsetHeight + 16;
          }
          hl.style.width = "100%%";
          hl.style.position = "absolute";

          page.insertBefore(hl, page.firstChild);
          requestAnimationFrame(function() {
              hl.style.opacity = 0.3;
          });

      };

      window.addEventListener('hashchange', hashchange);
      window.addEventListener('resize', hashchange);
      hashchange();

    }