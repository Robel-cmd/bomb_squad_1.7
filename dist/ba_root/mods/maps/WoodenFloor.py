from __future__ import annotations

from typing import TYPE_CHECKING

import ba,_ba
from bastd.gameutils import SharedObjects
from bastd.actor.playerspaz import PlayerSpaz
import copy
if TYPE_CHECKING:
    from typing import Any, List, Dict

class mapdefs:
    points = {}
    # noinspection PyDictCreation
    boxes = {}
    boxes['area_of_interest_bounds'] = (0.0, 1.185751251, 0.4326226188) + (
        0.0, 0.0, 0.0) + (29.8180273, 11.57249038, 18.89134176)
    boxes['edge_box'] = (-0.103873591, 0.4133341891, 0.4294651013) + (
        0.0, 0.0, 0.0) + (22.48295719, 1.290242794, 8.990252454)
    points['ffa_spawn1'] = (-0.08015551329, 0.02275111462,
                            -4.373674593) + (8.895057015, 1.0, 0.444350722)
    points['ffa_spawn2'] = (-0.08015551329, 0.02275111462,
                            4.076288941) + (8.895057015, 1.0, 0.444350722)
    points['flag1'] = (-10.99027878, 0.05744967453, 0.1095578275)
    points['flag2'] = (11.01486398, 0.03986567039, 0.1095578275)
    points['flag_default'] = (-0.1001374046, 0.04180340146, 0.1095578275)
    boxes['goal1'] = (12.22454533, 1.0,
                    0.1087926362) + (0.0, 0.0, 0.0) + (2.0, 2.0, 12.97466313)
    boxes['goal2'] = (-12.15961605, 1.0,
                    0.1097860203) + (0.0, 0.0, 0.0) + (2.0, 2.0, 13.11856424)
    boxes['map_bounds'] = (0.0, 1.185751251, 0.4326226188) + (0.0, 0.0, 0.0) + (
        42.09506485, 22.81173179, 29.76723155)
    points['powerup_spawn1'] = (5.414681236, 0.9515026107, -5.037912441)
    points['powerup_spawn2'] = (-5.555402285, 0.9515026107, -5.037912441)
    points['powerup_spawn3'] = (5.414681236, 0.9515026107, 5.148223181)
    points['powerup_spawn4'] = (-5.737266365, 0.9515026107, 5.148223181)
    points['spawn1'] = (-10.03866341, 0.02275111462, 0.0) + (0.5, 1.0, 4.0)
    points['spawn2'] = (9.823107149, 0.01092306765, 0.0) + (0.5, 1.0, 4.0)
    points['tnt1'] = (-0.08421587483, 0.9515026107, -0.7762602271)
class WoodenFloor(ba.Map):
    """Stadium map for football games."""
    defs = mapdefs
    defs.points['spawn1'] = (-12.03866341, 0.02275111462, 0.0) + (0.5, 1.0, 4.0)
    defs.points['spawn2'] = (12.823107149, 0.01092306765, 0.0) + (0.5, 1.0, 4.0)
    name = 'Wooden Floor'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'football', 'team_flag', 'keep_away']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'footballStadiumPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {

            'model_bg': ba.getmodel('doomShroomBG'),
            'bg_vr_fill_model': ba.getmodel('natureBackgroundVRFill'),
            'collide_model': ba.getcollidemodel('bridgitLevelCollide'),
            'tex': ba.gettexture('bridgitLevelColor'),
            'model_bg_tex': ba.gettexture('doomShroomBGColor'),
            'collide_bg': ba.getcollidemodel('natureBackgroundCollide'),
            'railing_collide_model':
                (ba.getcollidemodel('bridgitLevelRailingCollide')),
            'bg_material': ba.Material()
        }
        data['bg_material'].add_actions(actions=('modify_part_collision',
                                                 'friction', 10.0))
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bg'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex']
            })
        ba.newnode('terrain',
                   attrs={
                       'model': self.preloaddata['bg_vr_fill_model'],
                       'lighting': False,
                       'vr_only': True,
                       'background': True,
                       'color_texture': self.preloaddata['model_bg_tex']
                   })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.3, 1.2, 1.0)
        gnode.ambient_color = (1.3, 1.2, 1.0)
        gnode.vignette_outer = (0.57, 0.57, 0.57)
        gnode.vignette_inner = (0.9, 0.9, 0.9)
        gnode.vr_camera_offset = (0, -0.8, -1.1)
        gnode.vr_near_clip = 0.5
        # self.map_extend()

    def is_point_near_edge(self,
                           point: ba.Vec3,
                           running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

    def map_extend(self):
        pass
        # p=[-6,-4.3,-2.6,-0.9,0.8,2.5,4.2,5.9]
        # q=[-4,-2.3,-0.6,1.1,2.8,4.5,6.2]
        # for i in p:
        #     for j in q:
        #         self.create_ramp(i,j)

        # self.create_ramp(10.9)
        # self.ground()

    def ground(self):
        shared = SharedObjects.get()
        self._real_wall_material=ba.Material()

        self._real_wall_material.add_actions(

            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', True)

            ))
        self.mat = ba.Material()
        self.mat.add_actions(

            actions=( ('modify_part_collision','physical',False),
                      ('modify_part_collision','collide',False))
            )
        spaz_collide_mat=ba.Material()
        spaz_collide_mat.add_actions(
            conditions=('they_have_material',shared.player_material),
            actions=(
                ('modify_part_collision', 'collide', True),
                ( 'call','at_connect',ba.Call(self._handle_player_collide )),
            ),
            )
        pos=(0,0.1,-5)
        self.main_region=ba.newnode('region',attrs={'position': pos,'scale': (21,0.001,20),'type': 'box','materials': [shared.footing_material,self._real_wall_material,spaz_collide_mat]})


    def create_ramp_111(self,x,z):

        shared = SharedObjects.get()
        self._real_wall_material=ba.Material()

        self._real_wall_material.add_actions(

            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', True)

            ))
        self.mat = ba.Material()
        self.mat.add_actions(

            actions=( ('modify_part_collision','physical',False),
                      ('modify_part_collision','collide',False))
            )
        spaz_collide_mat=ba.Material()

        pos=(x,0,z)
        ud_1_r=ba.newnode('region',attrs={'position': pos,'scale': (1.5,1,1.5),'type': 'box','materials': [shared.footing_material,self._real_wall_material ]})

        node = ba.newnode('prop',
                                    owner=ud_1_r,
                                    attrs={
                                    'model':ba.getmodel('image1x1'),
                                    'light_model':ba.getmodel('powerupSimple'),
                                    'position':(2,7,2),
                                    'body':'puck',
                                    'shadow_size':0.0,
                                    'velocity':(0,0,0),
                                    'color_texture':ba.gettexture('tnt'),
                                    'model_scale':1.5,
                                    'reflection_scale':[1.5],
                                    'materials':[self.mat, shared.object_material,shared.footing_material],
                                    'density':9000000000
                                    })
        mnode = ba.newnode('math',
                               owner=ud_1_r,
                               attrs={
                                   'input1': (0, 0.6, 0),
                                   'operation': 'add'
                               })


        node.changerotation(1,0,0)
        ud_1_r.connectattr('position', mnode, 'input2')
        mnode.connectattr('output', node, 'position')




    def _handle_player_collide(self):
        try:
            player = ba.getcollision().opposingnode.getdelegate(
                PlayerSpaz, True)
        except ba.NotFoundError:
            return


        if player.is_alive():
            player.shatter(True)




ba._map.register_map(WoodenFloor)
