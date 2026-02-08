## 3D Software Renderer (From Scratch)

This repository contains a small 3D software renderer written in Python using Pygame.  
The goal of this project was to understand how a traditional 3D graphics pipeline works internally, without using OpenGL, DirectX, or external rendering libraries.

One of the core parts of this project is a **custom implementation of triangle clipping**.  
Triangles that fall partially outside the view volume are manually clipped and split using geometric intersection calculations in normalized device coordinates.

### What’s implemented
- Camera transformations and movement
- Perspective projection
- Back-face culling
- **Custom triangle clipping against screen boundaries**
- Basic triangle rasterization
- Real-time interaction

This project helped me gain a deeper understanding of how rendering engines handle geometry before rasterization.

## Demo

<p align="center">
  <img src="images/render.gif" width="500" />
</p>

*Software rendering with custom triangle clipping*
