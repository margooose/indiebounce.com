document.addEventListener('visibilitychange', function() {
    console.log(document.visibilityState);
    if (document.visibilityState === 'hidden') {
    var userQuitData = new FormData();
    userQuitData.append('csrfmiddlewaretoken', '{{csrf_token}}');
    userQuitData.append('userHidden', 4);
    navigator.sendBeacon("{% url 'main:playGameSegment' game.pk gsegment.pk %}",userQuitData)};
  if (document.visibilityState === 'hidden') {
    var userQuitData = new FormData();
    userQuitData.append('csrfmiddlewaretoken', '{{csrf_token}}');
    userQuitData.append('userHidden', 4);
    navigator.sendBeacon("{% url 'main:playGameSegment' game.pk gsegment.pk %}",userQuitData);
    }})