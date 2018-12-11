/**
 * param 将要转为URL参数字符串的对象
 * key URL参数字符串的前缀
 * encode true/false 是否进行URL编码,默认为true
 *
 * return URL参数字符串
 */

// Object.prototype.length = function() {
//     var count = 0;
//     for(var i in this){
//         count ++;
//      }
//     return count;
//  };

export default function urlEncode(paramObj, encode) {
  if(paramObj==null) return '';
  var paramArr = new Array()
  var t = typeof (paramObj);
  if (t === 'object') {
    for (var key in paramObj) {
      paramArr.push(key.toString() + '=' + ((encode==null||encode) ? encodeURIComponent(paramObj[key].toString()) : paramObj[key].toString()))
    }
    return '?' + paramArr.join('&')
  } else {
    return ''
  }
}
