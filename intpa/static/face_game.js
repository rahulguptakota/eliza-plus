$(document).ready(function(){
var time = 0;
var running = 1;
var done = 0;
increment();

function reset(){
	time =0;
	running =1;
	done = 0;
}
function increment()
{
    if(running == 1){
        setTimeout(function(){
            time++;
            // console.log(time);
            var mins = Math.floor(time/10/60);
            var secs = Math.floor(time/10 % 60);
            var tenths = time % 10;
           
            // if(mins < 10){
            //         mins = mins;
            // }
            // if(secs < 10){
            //         secs = secs;
            // }
            document.getElementById("stopwatch").innerHTML = mins + ":" + secs + ":" +  tenths ;
            if(level == 1 && time>40 && done==0){
				score = score -1;
				done = 1;
			}
			else if(level==2 && time>20 && done==0){
				score = score - 1;
				done = 1;
			}
			else if(level ==3 && time>10 && done==0){
				score = score -1;
				done = 1;
			}
			document.getElementById('score_value').innerHTML = score;
            increment();
               
        },100);
    }
}

var memory_array = ['A','B','C','D'];

Array.prototype.memory_tile_shuffle = function(){
    var i = this.length, j, temp;
    while(--i > 0){
        j = Math.floor(Math.random() * (i+1));
        temp = this[j];
        this[j] = this[i];
        this[i] = temp;
    }
}

var ans =0;
var opt=0;
var level = 1;
var output = '';
var source1, source2, source3, source4;
var score = parseInt($('h3#score_value').html()) - 1;
var user_id = parseInt($('div#hidden.user_id').html());
var con_correct =-1; //consecutive correct answers
var con_wrong = 0;
var correct = 1;
$.ajax({
	type: "GET",
	url: '/facegame/getimages/', 
	data: { user_level: level }, 
	// beforesend: function(xhr){
	// 	// console.log("adfds");
	// 	xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
	// },
	success: function(data)
	{
		source1 = data[0];
		source2 = data[1];
		source3 = data[2];
		source4 = data[3];
		output = '';
	    memory_array.memory_tile_shuffle();
	    for(var i = 0; i < memory_array.length; i++){
	    	if(memory_array[i] == 'A'){
				ans = i;
			}
	    }
	    for(var i = 0; i < memory_array.length; i++){
			if(memory_array[i] == 'A'){
				source = source1;
				// source = document.getElementById("hidden").getAttribute("src")+"/happy/p"+Math.floor(Math.random() * (totalh));
			}
			else if(memory_array[i] == 'B'){
				source = source2;
				// source = document.getElementById("hidden").getAttribute("src")+"/sad/p"+Math.floor(Math.random() * (totals));
			}
			else if(memory_array[i] == 'C'){
				source = source3;
				// source = document.getElementById("hidden").getAttribute("src")+"/angry/p"+Math.floor(Math.random() * (totala));
			}
			else{
				source = source4;
				// source = document.getElementById("hidden").getAttribute("src")+"/neutral/p"+Math.floor(Math.random() * (totaln));
			}
			output += '<div id=\"tile_'+i+'\"><img src=\"'+source+'\" height=\"100%\" width=\"100%\"></img></div>';
			// document.getElementById("tile_"+i).onclick = happyClick(i, ans);
		}
		reset();					
		document.getElementById('memory_board').innerHTML = output;
		document.getElementById('score_value').innerHTML = score;
    	document.getElementById("tile_0").addEventListener ("click", function(){ opt =0;myfunc(); } , false);
		document.getElementById("tile_1").addEventListener ("click", function(){ opt = 1;myfunc(); } , false);
		document.getElementById("tile_2").addEventListener ("click", function(){ opt = 2;myfunc(); } , false);
		document.getElementById("tile_3").addEventListener ("click", function(){ opt = 3;myfunc(); } , false);

	},
	error: function(xhr, ermsg,err){
		alert(xhr.status + ": " + xhr.responseText);
	}

});
function myfunc(){
	// running=0;
	if(ans == opt){
		if(level == 1) score = score + 1;
		else if(level ==2) score  = score + 2;
		else score = score + 3;
		con_wrong=0;
		con_correct = con_correct + 1;
		if(con_correct ==8){
			if(level<3){
				level++;
			}
			con_correct = 0;
		}
	}
	else{
		con_correct =0;
		con_wrong++;
		// correct =0;
		score = score - 2;

		if(con_wrong ==3){
			if(level>1) level--;
			con_wrong=0;
		}
		document.getElementById('score_value').innerHTML = score;
	}		
	$.ajax({
		type: "POST",
		url: '/facegame/sendinfo/',
		data: 
		{	
			user_id: user_id,
			user_level: level,
			user_score: score,
		},
		// beforesend: function(xhr){
		// 	// console.log("adfds");
		// 	xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
		// },
		beforeSend: function(xhr){
			console.log("reaching the beforesend");
			xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
		},
		success: function(data)
		{	
			console.log("abcd");
			if(data){
				console.log("Server Error");
			}
		},
		error: function(xhr, ermsg,err){
			alert(xhr.status + ": " + xhr.responseText);
		}
	});
	$.ajax({
		type: "GET",
		url: '/facegame/getimages/', 
		data: { user_level: level }, 
		success: function(data)
		{
			source1 = data[0];
			source2 = data[1];
			source3 = data[2];
			source4 = data[3];
			output = '';
		    memory_array.memory_tile_shuffle();
		    for(var i = 0; i < memory_array.length; i++){
		    	if(memory_array[i] == 'A'){
					ans = i;
				}
		    }
		    for(var i = 0; i < memory_array.length; i++){
				if(memory_array[i] == 'A'){
					source = source1;
					// source = document.getElementById("hidden").getAttribute("src")+"/happy/p"+Math.floor(Math.random() * (totalh));
				}
				else if(memory_array[i] == 'B'){
					source = source2;
					// source = document.getElementById("hidden").getAttribute("src")+"/sad/p"+Math.floor(Math.random() * (totals));
				}
				else if(memory_array[i] == 'C'){
					source = source3;
					// source = document.getElementById("hidden").getAttribute("src")+"/angry/p"+Math.floor(Math.random() * (totala));
				}
				else{
					source = source4;
					// source = document.getElementById("hidden").getAttribute("src")+"/neutral/p"+Math.floor(Math.random() * (totaln));
				}
				output += '<div id=\"tile_'+i+'\"><img src=\"'+source+'\" height=\"100%\" width=\"100%\"></img></div>';
				// document.getElementById("tile_"+i).onclick = happyClick(i, ans);
			}
			reset();
			// increment();					
			document.getElementById('memory_board').innerHTML = output;
			document.getElementById('score_value').innerHTML = score;
	    	document.getElementById("tile_0").addEventListener ("click", function(){ opt =0;myfunc(); } , false);
			document.getElementById("tile_1").addEventListener ("click", function(){ opt = 1;myfunc(); } , false);
			document.getElementById("tile_2").addEventListener ("click", function(){ opt = 2;myfunc(); } , false);
			document.getElementById("tile_3").addEventListener ("click", function(){ opt = 3;myfunc(); } , false);

		}
    });
	
}
myfunc();
});