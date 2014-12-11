<style TYPE="text/css">
code.has-jax {font: inherit; font-size: 100%; background: inherit; border: inherit;}
</style>
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
    tex2jax: {
        inlineMath: [['$','$'], ['\(','\)']],
        skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'] // removed 'code' entry
    }
});
MathJax.Hub.Queue(function() {
    var all = MathJax.Hub.getAllJax(), i;
    for(i = 0; i < all.length; i += 1) {
        all[i].SourceElement().parentNode.className += ' has-jax';
    }
});
</script>
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>

Exploring Neural Data Final Project
===================================

## Description of the data

I used the visual processing data set for the final project. The data contained spike times of neural single units recorded in cortices of apes that were exposed to images which were flashed on a screen. The dataset was subdivided into spike times of images that caused a low response of neurons [ineffective targets] and spike times of images that a caused high response of neurons [effective targets]. I filtered the data by sorting the spiketimes of the single units according to their respective picture.

## Question addressed in the project

I calculated the average frequency of neurons within discrete time intervalls of 100 ms in order to find higher order patterns of neural response. I hypothesized that the collecive response of the single units may establish a distinct frequency pattern that is specific for ineffectiv or effevtive targets, respectively. Therefore, I wrote a extensive python script that visualizes the neural response of the single units in form of histograms and scatter plots.     

## Figures

![](https://raw.githubusercontent.com/sagar87/Exploring-Neural-Data-Final-Project/master/survey%20data/sur1billiards00.png)![](https://raw.githubusercontent.com/sagar87/Exploring-Neural-Data-Final-Project/master/survey%20single%20unit/sur1subilliards00.png)