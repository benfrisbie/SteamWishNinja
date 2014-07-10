$.getJSON('/topgamesontwitch', function(data){
  console.log(data.top[0].game.name);
});
