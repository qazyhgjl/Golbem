#version 120

// Sci-Fi Medical Fragment Shader with Fresnel Glow & PBR Rim Lighting
varying vec3 vNormal;
varying vec3 vPosition;
varying vec3 vEyeVector;

uniform vec4 uMaterialColor;
uniform vec3 uKeyLightDir;
uniform vec3 uKeyLightColor;
uniform vec3 uFillLightColor;
uniform vec3 uRimColor;
uniform float uFresnelPower;
uniform float uSpecularShininess;
uniform float uAlpha;

void main() {
    vec3 N = normalize(vNormal);
    vec3 V = normalize(vEyeVector);
    vec3 L = normalize(uKeyLightDir);
    vec3 H = normalize(L + V);

    // Diffuse shading
    float NdotL = max(dot(N, L), 0.0);
    vec3 diffuseKey = uKeyLightColor * NdotL;

    // Fill light (opposite direction)
    float NdotFill = max(dot(N, -L), 0.0) * 0.4;
    vec3 diffuseFill = uFillLightColor * NdotFill;

    // Specular highlight
    float NdotH = max(dot(N, H), 0.0);
    float spec = pow(NdotH, uSpecularShininess);
    vec3 specular = vec3(1.0) * spec * 0.6;

    // Sci-Fi Fresnel Rim Lighting (Edge Glow)
    float fresnel = 1.0 - max(dot(N, V), 0.0);
    fresnel = pow(fresnel, uFresnelPower);
    vec3 rimGlow = uRimColor * fresnel * 1.2;

    // Final color synthesis
    vec3 finalRGB = uMaterialColor.rgb * (diffuseKey + diffuseFill + vec3(0.15)) + specular + rimGlow;
    float finalAlpha = clamp(uMaterialColor.a * uAlpha + fresnel * 0.25, 0.0, 1.0);

    gl_FragColor = vec4(finalRGB, finalAlpha);
}
