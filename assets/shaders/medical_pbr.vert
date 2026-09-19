#version 120

// Sci-Fi Medical Vertex Shader
varying vec3 vNormal;
varying vec3 vPosition;
varying vec3 vEyeVector;

void main() {
    vNormal = normalize(gl_NormalMatrix * gl_Normal);
    vec4 vertPos = gl_ModelViewMatrix * gl_Vertex;
    vPosition = vertPos.xyz;
    vEyeVector = normalize(-vertPos.xyz);

    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
