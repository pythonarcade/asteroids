uniform vec2 pos;

vec2 Hash12(float t) {
  float x = fract(sin(t * 674.3)*453.2);
  float y = fract(sin((t+x) * 724.3)*341.2);
  return vec2(x, y);
}
vec2 Hash12_Polar(float t) {
  float a = fract(sin(t * 674.3)*453.2)*6.2832;
  float d = fract(sin((t+a) * 724.3)*341.2);

  return vec2(sin(a), cos(a)) * d;
}
void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 npos = (pos-.5*iResolution.xy)/iResolution.y;
    vec2 uv = (fragCoord-.5*iResolution.xy)/iResolution.y;
//    vec2 uv = fragCoord/iResolution.xy;
    uv -= npos;
    float col = 0.;
    vec3 baseColor = vec3(1., 0., 0.);

    float t = fract(iTime);

    for (float i=0.;i<125.;i++) {
        vec2 dir = Hash12_Polar(i+1.0);

        float d = length(uv - dir * t);
        float brightness = mix(.0005, .002, smoothstep(.1, 0., t));

        brightness *= sin(t*20.+i)*.5+.5;
        col += brightness/d;
    }
    // Output to screen
    fragColor = vec4(1.0, 1.0, 1.0, col * (1.0 - t));
}
